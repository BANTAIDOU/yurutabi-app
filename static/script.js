const swiper = new Swiper('.swiper', {
  loop: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

function goToRandomMap() {
  const maps = [
    'https://tomo-shintk.github.io/yurutabi-site/oseania.html',
    'https://tomo-shintk.github.io/yurutabi-site/europe.html',
    'https://tomo-shintk.github.io/yurutabi-site/asia.html',
    'https://tomo-shintk.github.io/yurutabi-site/northamerica.html'
  ];
  const randomUrl = maps[Math.floor(Math.random() * maps.length)];
  window.open(randomUrl, '_blank');
}
