$("form").on("change", ".campo-archivo",function(){
	$(this).parent(".zona-de-subida").attr("data-text",$(this).val().replace(/.*(\/|\\)/,''));
})