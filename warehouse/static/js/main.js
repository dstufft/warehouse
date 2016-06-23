$(document).ready(function() {

  // Look for any data-html-include elements, and include the content for them
  $('[data-html-include]').each(function() {
    $(this).load($(this).data('html-include'));
  });

  // Toggle expanding and collapsing sections
  $('.-js-expander-trigger').click(function(){
    $(this).toggleClass("expander-hidden");
  });

  $(".js-vertical-tab-content").hide();
  $(".js-vertical-tab-content:first").show();

  /* if in tab mode */
  $(".-js-vertical-tab").click(function(event) {
    event.preventDefault();

    $(".js-vertical-tab-content").hide();
    var activeTab = $(this).attr("rel");
    $("#"+activeTab).show();

    $(".-js-vertical-tab").removeClass("is-active");
    $(this).addClass("is-active");

    $(".-js-vertical-tab-accordion-heading").removeClass("is-active");
    $(".-js-vertical-tab-accordion-heading[rel^='"+activeTab+"']").addClass("is-active");
  });

  /* if in accordion mode */
  $(".-js-vertical-tab-accordion-heading").click(function(event) {
    event.preventDefault();

    $(".js-vertical-tab-content").hide();
    var accordion_activeTab = $(this).attr("rel");
    $("#"+accordion_activeTab).show();

    $(".-js-vertical-tab-accordion-heading").removeClass("is-active");
    $(this).addClass("is-active");

    $(".-js-vertical-tab").removeClass("is-active");
    $(".-js-vertical-tab[rel^='"+accordion_activeTab+"']").addClass("is-active");
  });

  // Launch filter popover on mobile
  $('body').on('click', '.-js-add-filter', function(e){
    e.preventDefault();
    $('.dark-overlay').show();
    $('.panel-overlay').show();
  });

  $('body').on('click', '.-js-close-panel', function(e){
    e.preventDefault();
    $('.dark-overlay').hide();
    $('.panel-overlay').hide();
  });

  // Position Sticky bar
  function positionWarning(){
    var height = $('.sticky-bar').outerHeight();
    $('body:has(.sticky-bar)').css('paddingTop', height);
  }

  positionWarning();

  $(window).resize(function(){
    positionWarning();
  });

  // document.l10n.ready.then(function() {
  //   // Format all of the time.relative tags to display relative time.
  //   $(".-js-relative-time").timeago();
  // });
  $(".-js-relative-time").timeago();  // Add back to document.l10n.ready

  // Load the stats pane
  $(".-js-stats-pane").each(function() {
    var url = $(this).data('url');
    var toReplace = $(this);

    function fetchStats() {
      $.ajax( url )
       .done(function(data, textStatus, jqXHR) {
         if (jqXHR.status == 202) {
            setTimeout(fetchStats, 1000);
         } else if (jqXHR.status == 200) {
            toReplace.html(data);
         }
       });
    }

    fetchStats();

  });

});
