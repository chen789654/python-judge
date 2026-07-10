// Python Judge 前端交互

document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏 Flash 消息
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 确认删除操作
    document.querySelectorAll('[data-confirm]').forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm') || '确定要执行此操作吗？')) {
                e.preventDefault();
            }
        });
    });
});
