function photobooth_start(){
	$(".photobooth_alert").hide();
	$('#photobooth').show();
	if (! $('#photobooth').data("photobooth")) {
		$('#photobooth').photobooth();

		if( !$( '#photobooth' ).data( "photobooth" ).isSupported ){
			alert("Webcam/Browser not supported")
		}

		$('#photobooth').on("image", function (event, dataUrl) {
			$("#photopreview").show().html('<img src="' + dataUrl + '" >');
			$("#photobooth_image").val(dataUrl);
			$(".photobooth_alert").show();
			$('#photobooth').data("photobooth").pause();
			$('#photobooth').hide();
		});
	} else {
		$('#photobooth').data("photobooth").resume();
	}
}
$(document).ready(function(){
	//alert($('.photobooth_image').value);
	value = $('#photobooth_image').val();
	if(value.startsWith("data:image/png;base64")){
		$( "#photopreview" ).show().html( '<img src="' + value + '" >');
	}
	$(".photobooth_alert").show();

    //$( '#photobooth' ).data( "photobooth" ).forceHSB = true;
});