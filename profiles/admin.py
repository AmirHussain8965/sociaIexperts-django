from django.contrib import admin
from django.contrib import messages
from .models import Wallet, Transaction, Earning, UserPlan, ReferralBonus, ReferralProfile, ReferralRecord
from .signals import recalculate_wallet_balance


@admin.register(ReferralBonus)
class ReferralBonusAdmin(admin.ModelAdmin):
    """Singleton — admin sets the referral reward amount."""
    list_display = ('amount',)

    def has_add_permission(self, _request):
        return not ReferralBonus.objects.exists()

    def has_delete_permission(self, _request, _obj=None):
        return False


@admin.register(ReferralProfile)
class ReferralProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'get_total_referrals', 'get_total_earned', 'created_at')
    search_fields = ('user__username', 'code')
    readonly_fields = ('code', 'created_at')

    @admin.display(description='Referrals')
    def get_total_referrals(self, obj):
        return obj.total_referrals

    @admin.display(description='Total Earned')
    def get_total_earned(self, obj):
        return f'${obj.total_earned}'


@admin.register(ReferralRecord)
class ReferralRecordAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred', 'reward_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('referrer__username', 'referred__username')
    readonly_fields = ('referrer', 'referred', 'reward_amount', 'created_at')
    ordering = ('-created_at',)


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'is_active', 'activated_at')
    list_filter = ('is_active', 'package')
    search_fields = ('user__username', 'user__email')
    list_editable = ('is_active',)
    autocomplete_fields = ()
    ordering = ('-activated_at',)


@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'amount', 'note', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('wallet__user__username', 'wallet__user__email', 'note')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    @admin.display(description='User', ordering='wallet__user__username')
    def get_username(self, obj):
        return obj.wallet.user.username


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'get_username', 'transaction_type', 'amount',
        'get_bank_label', 'account_number', 'status', 'created_at',
    )
    list_filter = ('transaction_type', 'status', 'bank_type', 'created_at')
    search_fields = ('wallet__user__username', 'wallet__user__email', 'account_number', 'bank_name', 'note')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    actions = ['approve_withdrawal_requests', 'reject_withdrawal_requests']

    # ── Display helpers ──────────────────────────────────────────────

    @admin.display(description='User', ordering='wallet__user__username')
    def get_username(self, obj):
        return obj.wallet.user.username

    @admin.display(description='Payment Method')
    def get_bank_label(self, obj):
        if obj.bank_type == 'other' and obj.bank_name:
            return obj.bank_name
        return obj.get_bank_type_display() if obj.bank_type else '—'

    # ── Admin actions ────────────────────────────────────────────────

    @admin.action(description='Approve selected withdrawal requests')
    def approve_withdrawal_requests(self, request, queryset):
        eligible = queryset.filter(transaction_type='withdrawal', status='pending')
        count = 0
        for txn in eligible:
            txn.status = 'completed'
            txn.save()          # triggers post_save signal → recalculates balance
            count += 1
        if count:
            self.message_user(request, f'{count} withdrawal(s) approved and balance updated.', messages.SUCCESS)
        else:
            self.message_user(request, 'No pending withdrawal requests were selected.', messages.WARNING)

    @admin.action(description='Reject selected withdrawal requests')
    def reject_withdrawal_requests(self, request, queryset):
        eligible = queryset.filter(transaction_type='withdrawal', status='pending')
        count = 0
        for txn in eligible:
            txn.status = 'failed'
            txn.save()
            count += 1
        if count:
            self.message_user(request, f'{count} withdrawal(s) rejected.', messages.WARNING)
        else:
            self.message_user(request, 'No pending withdrawal requests were selected.', messages.WARNING)
