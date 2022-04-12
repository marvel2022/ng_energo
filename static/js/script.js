
window.replainSettings = { id: 'b1923618-b1a2-4b7d-8025-f5ea89ae7496' };
(function(u){var s=document.createElement('script');s.type='text/javascript';s.async=true;s.src=u;
var x=document.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);
})('https://widget.replain.cc/dist/client.js');

  
  // Preloader
  $(window).on('load', function() {
    if ($('#preloader').length) {
      $('#preloader').delay(300).fadeOut('slow', function() {
        $(this).remove();
      });
    }
  });

  // Crol to top
  var $btnTop = $(".btn-top");
  $(window).on("scroll",function(){
    if($(window).scrollTop() >= 20)
    {
      $btnTop.fadeIn();
    }
    else{
      $btnTop.fadeOut();
    }
  });
  $btnTop.on("click",function(){
    $("html,body").animate({scrollTop:0},1200)
  });


$(document).ready(function(){


  var counters = $(".count");
  var countersQuantity = counters.length;
  var counter = [];

  for (i = 0; i < countersQuantity; i++) {
    counter[i] = parseInt(counters[i].innerHTML);
  }

  var count = function(start, value, id) {
    var localStart = start;
    setInterval(function() {
      if (localStart < value) {
        localStart++;
        counters[id].innerHTML = localStart;
      }
    }, 40);
  }

  for (j = 0; j < countersQuantity; j++) {
    count(0, counter[j], j);
  }

    });

$(document).ready(function(){

    $('.customer-logos').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3500,
        arrows: false,
        dots: false,
        pauseOnHover: false,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
                slidesToShow: 3
            }
        },{
            breakpoint: 768,
            settings: {
                slidesToShow: 2
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 1
            }
        }]
    });

});


