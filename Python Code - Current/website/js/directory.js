$(document).ready(function() {
	// filter the demo list when the filter links are clicked
	$('#tag-list li a').live('click',function(e){

		//var getText = $(this).text().replace(" ", "-");
		//var getText = $(this).text();
		var getText = $(this).get(0).id;
		if(getText == 'all'){
			$("#demo-list li a").slideDown();
		} else {
			$("#demo-list li a").fadeOut();
			$("#demo-list li a."+getText).fadeIn();
		}
		
		// add class "active" to current filter item
		$('#tag-list li a').removeClass('active');
		$(this).addClass('active');
		
		// prevent the page scrolling to the top of the screen
		e.preventDefault();
	});		
});
