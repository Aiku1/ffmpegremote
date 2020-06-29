var filename = '';
var inputfile = '';
var container = '';
var v_codec = '';
var abr = 0;
var mbr = 0;
var scale = '';
var trim = false;
var ss = 0;	//enhance performance: https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video
var to = 0;	
var preset = 0;
var profile = 0;
var presetNames = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'];
var dnx_bitrates = [36, 60, 90, 120, 185];
var a_codec = '';
var a_br = 0;

var outputfile_string = '_converted';
var outputfile = '';

var videostring = '';
var audiostring = '';
var finalstring = '';

var filesize = 0;
var length = '';

function update(){
	
	//video string
	trim = $("input[name='trim']").prop('checked');
	ss = $("#ss").val();
	to = $("#to").val();

	if(trim == true){
		$("#ss").prop('disabled', false).parent().removeClass('unable');
		$("#to").prop('disabled', false).removeClass('unable');
		videostring = ' -ss ' + ss +
					  ' -to ' + to;
	} else {
		$("#ss").prop('disabled', true).parent().addClass('unable');
		$("#to").prop('disabled', true).addClass('unable');
		videostring = '';
	}

	v_codec = $("select[name='v_codec']").val();

	$('.disabled').not('#fc').removeClass('disabled');

	//clean up code
	//? help buttons
	//right audio codec for dnxhd

	if
	(v_codec == 'copy'){
		$('.videoAdjustment').addClass('disabled');
		videostring = videostring + ' -c:v ' + v_codec + ' ';
	} else if 
	(v_codec == 'prores'){
		$('#container select').val('mov');
		$("select[name='a_codec']").val('aac');
		$('#container, #bitrate, #preset input, #presetName, #dnxPresets').addClass('disabled');
		profile = $("select[name='profile']").val();
		scale = $("select[name='scale']").val();
		videostring = videostring +
					  ' -c:v ' + v_codec + 
					  ' -profile:v ' + profile;
		if(scale!=0){videostring = videostring + ' -vf scale=' + scale};
	} else if 
	(v_codec == 'dnxhd'){
		$('#container select').val('mov');
		$("select[name='a_codec']").val('pcm_s16le');
		$('.bitrates_normal, #proresPresets, #preset input, #presetName').addClass('disabled');
		$('#slider1').change(function() {
		    $('span').text(values[this.value]);
		});
		profile = $("select[name='dnxprofile']").val();
		abr = dnx_bitrates[$("input[name='dnxbr']").val()] + 'M';
		videostring = videostring +
					  ' -c:v ' + v_codec + 
					  ' -profile:v ' + profile +
					  ' -b:v ' + abr;
		if(scale!=0){videostring = videostring + ' -vf scale=' + scale};
	} else { 
		$('#proresPresets, .bitrate_dnx, #dnxPresets').addClass('disabled');
		$("select[name='a_codec']").val('aac');
		abr = $("input[name='abr']").val() + 'M';
		mbr = $("input[name='mbr']").val() + 'M';
		preset = $("input[name='preset']").val();
		scale = $("select[name='scale']").val();
		constant = $("input[name='constant']").prop('checked');
		if(constant == true){
			$(".vbr").addClass('disabled');
			var constantBitrate = $("input[name='cbr']").val() + 'M';
			abr = constantBitrate;
			mbr = constantBitrate + ' -maxrate ' + constantBitrate;
		} else {
			$(".cbr").addClass('disabled');
		}
		var presetName = presetNames[preset];
		videostring = 	videostring +
						' -c:v ' + v_codec + 
						' -b:v ' + abr + 
						' -minrate ' + mbr +
						' -preset ' + presetName;
		if(scale!=0){videostring = videostring + ' -vf scale=' + scale};
	};

	//audio string
	a_codec = $("select[name='a_codec']").val();

	if(a_codec == 'copy' || a_codec == 'pcm_s16le'){
		$('.audioAdjustment').addClass('disabled');
		audiostring = ' -c:a ' + a_codec;
	} else if(a_codec==0){
		$('.audioAdjustment').addClass('disabled');
		audiostring = ' -an ';
	} else {
		$('.audioAdjustment').removeClass('disabled');
		a_br = $("input[name='brA']").val() + 'K';
		audiostring = 	' -c:a ' + a_codec +
						' -b:a ' + a_br;
	};

	// Filesize Calculator
	length = hmsToSeconds($('#lengthFC').val());
	filesize = ($("input[name='abr']").val() * length / 8) + ($("input[name='brA']").val() / 1024 * length / 8);
	$('#finalsize').html(filesize.toFixed(2));

	//filename strings
	inputfile = $("input[name='input_filename']").val().split(/(\\|\/)/g).pop();
	filename = inputfile.split('.')[0];
	container = $("select[name='container']").val();
	outputfile = ' ' + filename + outputfile_string + '.' + container;
	
	//final string
	finalstring = 'ffmpeg -i ' + inputfile + videostring + audiostring + outputfile;
	$("#final_string").val(finalstring);
};

$('#form').change(function(){
	update();
});

$('#dnxbrSlider').change(function(){
	var d_b = this.value;
	$('#dnxbr_number').html(dnx_bitrates[d_b]);
})

$('#presetSlider').change(function(){
	var p_i = this.value;
	$('#presetName').html(presetNames[p_i]);
})

$('#openFC').on('click', function(){
	$('#fc').toggleClass('disabled');
})

function hmsToSeconds(str) {
    var p = str.split(':'),
        s = 0, m = 1;
    while (p.length > 0) {
        s += m * parseInt(p.pop(), 10);
        m *= 60;
    }
    return s;
}