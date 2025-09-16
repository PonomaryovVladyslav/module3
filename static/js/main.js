// Basic interactivity for messages and small UI touches
(function(){
  // Close messages on click of X
  document.addEventListener('click', function(e){
    if (e.target && e.target.matches('[data-close-message]')){
      const item = e.target.closest('.message');
      if (item) item.remove();
    }
  });

  // Auto-dismiss messages after 4 seconds
  const msgs = document.querySelectorAll('.message');
  msgs.forEach(function(m){
    setTimeout(function(){
      if (m && m.parentElement) m.remove();
    }, 4000);
  });
})();

  // Mobile nav toggle
  document.addEventListener('click', function(e){
    if (e.target && e.target.matches('[data-nav-toggle]')){
      const btn = e.target;
      const nav = document.querySelector('.nav-links');
      if (!nav) return;
      const isOpen = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    }
  });

