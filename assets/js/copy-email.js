document.addEventListener('DOMContentLoaded', function() {
  const copyButtons = document.querySelectorAll('[data-action="copy-email"]');

  copyButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const email = this.getAttribute('data-email');
      
      if (!email) return;

      navigator.clipboard.writeText(email).then(() => {
        showNotification("✅ Email address copied to clipboard");
      }).catch(err => {
        console.error('Failed to copy: ', err);
        // Fallback
        const textArea = document.createElement('textarea');
        textArea.value = email;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showNotification("✅ Email address copied to clipboard");
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
            alert('이메일 주소: ' + email);
        }
        document.body.removeChild(textArea);
      });
    });
  });

  function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.innerText = message;
    
    // Style the notification
    Object.assign(notification.style, {
      position: 'fixed',
      bottom: '20px',
      left: '50%',
      transform: 'translateX(-50%)',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      color: 'white',
      padding: '12px 24px',
      borderRadius: '5px',
      zIndex: '10000',
      opacity: '0',
      transition: 'opacity 0.3s ease-in-out',
      fontSize: '16px',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    });

    document.body.appendChild(notification);

    // Fade in
    requestAnimationFrame(() => {
      notification.style.opacity = '1';
    });

    // Remove after 3 seconds
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 300);
    }, 3000);
  }
});
