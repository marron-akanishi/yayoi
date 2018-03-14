onload = function(){
  var img = new Image();
  img.src = image_url;
  img.onload = function(){
    for(var i = 0; i < eval(facex).length; i++){
      var canvas = document.getElementById('canvas-'+i);
      var ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, Number(eval(facex)[i]), Number(eval(facey)[i]), Number(eval(facew)[i]), Number(eval(faceh)[i]));
    }
  }
}