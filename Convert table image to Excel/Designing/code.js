var modal = new bootstrap.Modal(document.getElementById("myModal"));

$.noConflict();
jQuery(document).ready(function ($) {
  $(".card .crop").click(function (e) {
    var s = $(this).parents(".card").find("img").attr("src");
    $("#ShowImg").attr("src", s);
    modal.show();
    ResizeImg();
  });

  $(window).on("load resize", ResizeImg);

  function ResizeImg() {
    var windowHeight = $(window).height() - 150;
    var windowWidth = $(window).width();
    var image = $("#ShowImg");

    var imageOriginalWidth = image[0].naturalWidth;
    var imageOriginalHeight = image[0].naturalHeight;

    var aspectRatio = imageOriginalWidth / imageOriginalHeight;

    image.height(windowHeight);
    image.width(windowHeight * aspectRatio);

    if (image.width() > windowWidth) {
      image.width(windowWidth);
      image.height(windowWidth / aspectRatio);
    }
    $("#mySVG").attr("width", image.width()).attr("height", image.height());

    var circle = $("circle"); // replace with the circle you want to move
    var x = Math.round($("#mySVG").height());
    var y = Math.round($("#mySVG").width());
    var loc = [
      [0, 0],
      [0, x],
      [y, x],
      [y, 0],
    ];
    // console.log(loc);
    for (var i = 0; i < circle.length; i++) {
      var cx = Math.round($(circle[i]).attr("cx"));
      var cy = Math.round($(circle[i]).attr("cy"));
      console.log(cx, cy);
      var l1 = $("line[x1=" + cx + "][y1=" + cy + "]");
      var l2 = $("line[x2=" + cx + "][y2=" + cy + "]");
      $(circle[i]).attr("cx", loc[i][0]);
      $(circle[i]).attr("cy", loc[i][1]);
      l1.attr("x1", $(circle[i]).attr("cx")).attr(
        "y1",
        $(circle[i]).attr("cy")
      );
      l2.attr("x2", $(circle[i]).attr("cx")).attr(
        "y2",
        $(circle[i]).attr("cy")
      );
    }
  }

  $(".card .delete").click(function (e) {
    $(this).parents(".card").remove();
  });

  $(".cloneCard:first").hide();

  $("#fileUpload").change(function (e) {
    for (var i = 0; i < e.target.files.length; i++) {
      (function (file) {
        var reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function (event) {
          var clon = $(".cloneCard:first").clone(true);
          clon.show();
          clon.find("img").attr("src", event.target.result);
          clon.appendTo("#asli");
          clon.find("h5").text(file.name.split(".")[0]);
        };
      })(e.target.files[i]);
    }
  });

  $("#ShowImg").click(function (event) {
    var renderedWidth = $(this).width();
    var originalWidth = $(this)[0].naturalWidth;

    var scaleX = originalWidth / renderedWidth;

    var x = event.offsetX * scaleX;
    var y = event.offsetY * scaleX; // assuming the image isn't stretched
    console.log("X Coordinate: " + x + ", Y Coordinate: " + y);
  });

  $("#mySVG").click(function (e) {
    var circle = $("circle[fill='red']"); // replace with the circle you want to move
    //for (var i = 0; i < circle.length; i++)
    if (circle.length > 0) {
      var cx = circle.attr("cx");
      var cy = circle.attr("cy");
      // if (!check(circle.attr("id"), e.offsetX, e.offsetY)) return;

      var l1 = $("line[x1=" + cx + "][y1=" + cy + "]");
      var l2 = $("line[x2=" + cx + "][y2=" + cy + "]");

      circle.attr("cx", e.offsetX);
      circle.attr("cy", e.offsetY);
      // update lines
      var renderedWidth = $("#ShowImg").width();
      var originalWidth = $("#ShowImg")[0].naturalWidth;

      var scaleX = originalWidth / renderedWidth;

      var x = e.offsetX * scaleX;
      var y = e.offsetY * scaleX; // assuming the image isn't stretched
      console.log("X Coordinate: " + x + ", Y Coordinate: " + y);
      
      l1.attr("x1", e.offsetX).attr("y1", e.offsetY);
      l2.attr("x2", e.offsetX).attr("y2", e.offsetY);
    }
  });

  $("circle").click(function (e) {
    var col = $(this).attr("fill");
    $("circle").attr("fill", "blue");
    if (col == "red") $(this).attr("fill", "blue");
    else $(this).attr("fill", "red");
  });

  function check(id, x, y, fasle = 10) {
    console.log(x, parseInt($("#circle2").attr("cx")));
    console.log(y, parseInt($("#circle4").attr("cy")));
    console.log(
      x + fasle < parseInt($("#circle2").attr("cx")) &&
        y + fasle < parseInt($("#circle4").attr("cy"))
    );
    if (id == "circle1") {
      if (
        x + fasle < parseInt($("#circle2").attr("cx")) &&
        y + fasle < parseInt($("#circle4").attr("cy"))
      )
        return true;
    } else if (id == "circle2") {
      if (
        x - fasle > parseInt($("#circle1").attr("cx")) &&
        y + fasle < parseInt($("#circle3").attr("cy"))
      )
        return true;
    } else if (id == "circle3") {
      if (
        x - fasle > parseInt($("#circle4").attr("cx")) &&
        y - fasle > parseInt($("#circle2").attr("cy"))
      )
        return true;
    } else {
      if (
        x + fasle < parseInt($("#circle3").attr("cx")) &&
        y - fasle > parseInt($("#circle1").attr("cy"))
      )
        return true;
    }
    return false;
  }
});
