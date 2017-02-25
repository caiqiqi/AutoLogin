(function(k) {
	$("input[value='10']").each(function(a, b) {
		$(b).prop("checked", true)
	});
	$("input[value='8']").each(function(a, b) {
		if (Math.random() > k) {
			$(b).prop("checked", true)
		}
	});
	$.post("pjPost.php", $("#pjForm").serialize(), function(b) {
		if (b.code != 0) {
			alert(b.info)
		} else {
			$("#actionPanel").html('<b>评教结果已经保存，您可以通过已评记录查询评价结果。<br><img width="400" src="http://congm.in/index/img/congminBlack.png" /></b>')
		}
	}, "json");
})(0.70);

<!-- from https://i.congm.in/xpj/ -->