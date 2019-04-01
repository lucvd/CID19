$(function () {

    $("#id_profilePicture").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#modalCrop").modal();
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    $("#linkedinpicture").click(function() {
        var request = new XMLHttpRequest();
        request.open('GET', $("#linkedinpicture").attr("src"), true);
        request.responseType = 'blob';
        request.onload = function() {
            var reader = new FileReader();
            reader.readAsDataURL(request.response);
            reader.onload =  function(e){
                $("#image").attr("src",e.target.result);
                $("#id_profilePicture").val('');
                $("#modalCrop").modal();
            };
        };
        request.send();
    });

    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 2,
            aspectRatio: 1/1,
            minCropBoxWidth: 300,
            minCropBoxHeight: 300,
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });


    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#formprofilepicture").submit();
    });


});

function download(dataurl, filename) {
    var a = document.createElement("a");
    a.href = dataurl;
    a.setAttribute("download", filename);
    var b = document.createEvent("MouseEvents");
    b.initEvent("click", false, true);
    a.dispatchEvent(b);
    return false;
}