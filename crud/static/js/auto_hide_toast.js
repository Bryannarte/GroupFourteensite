setTimeout(() => {
    document.querySelectorAll('.toast-success').forEach(toast => {
        toast.classList.add('opacity-0');
        setTimeout(() => toast.remove(), 500); // Wait for fade-out
    });
}, 3000);

document.querySelectorAll('.close-toast').forEach(btn => {
    btn.addEventListener('click', function() {
        const toast = this.closest('.toast-success');
        if (toast) {
            toast.classList.add('opacity-0');
            setTimeout(() => toast.remove(), 500);
        }
    });
});