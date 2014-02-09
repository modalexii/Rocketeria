def get(blobname,tags = None):

	if blobname == "whooffers":
		webcode = '''
				$('input:radio[name="services"]').change(
					function() {
						if ($(this).is(':checked')) {
							$.post("/lessons/api", {
								'request' : 'whooffers',
								'serviceid' : $(this).val(),
							})
							.done(function (data) {
								$(data).each(function(index) {
									$("#employee." + data[index]).show()
								});
								$("#employees").slideToggle("slow");
							})
							.fail(function(xhr, textStatus, errorThrown) {
								alert(textStatus + ': ' + errorThrown);
							});
						}
					}
				);
				  '''

	if tags == 'open':
		webcode = '<script type="text/javascript"> <!--\n$(document).ready(function(){\n' + webcode
	elif tags == 'openclose' :
		webcode = '<script type="text/javascript"><!--\n$(document).ready(function(){\n' + webcode +'\n});\n--> </script>'
	elif tags == 'close':
		webcode = webcode +' });\n-->\n</script>'
	elif tags == None:
		pass
	else:
		raise Exception('tags must be one of "open", "openclose", "close", or None')

	return webcode

'''
$(this).val()

$.post( "test.php", { name: "John", time: "2pm" })
  .done(function( data ) {
    alert( "Data Loaded: " + data );
  });

'''