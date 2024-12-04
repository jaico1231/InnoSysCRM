/*
Template Name: Admin Template
Author: Wrappixel

File: js
*/
// ==============================================================
// Auto select left navbar
// ==============================================================
///////////////////////////////////////////////////////////////////

function toggleMenu(menuId) {
  const menu = document.getElementById(menuId);
  if (menu.style.display === "none" || menu.style.display === "") {
      menu.style.display = "block";
  } else {
      menu.style.display = "none";
  }
}

window.addEventListener('DOMContentLoaded', (event) => {
  var url = window.location.href;
  var sidebarnav = document.getElementById('sidebarnav');
  var links = sidebarnav.getElementsByTagName('a');

  for (let i = 0; i < links.length; i++) {
      if (links[i].href === url) {
          links[i].classList.add('active');  // Resalta el enlace activo
          let parentMenu = links[i].closest('div');  // Encuentra el contenedor del menú padre
          if (parentMenu && parentMenu.style.display === "none") {
              parentMenu.style.display = "block";  // Despliega el menú si está colapsado
          }
      }
  }
});


// $(function () {
//     "use strict";
//     var url = window.location + "";
//     var path = url.replace(
//       window.location.protocol + "//" + window.location.host + "/",
//       ""
//     );
//     var element = $("ul#sidebarnav a").filter(function () {
//       return this.href === url || this.href === path; // || url.href.indexOf(this.href) === 0;
//     });
//     element.parentsUntil(".sidebar-nav").each(function (index) {
//       if ($(this).is("li") && $(this).children("a").length !== 0) {
//         $(this).children("a").addClass("active");
//         $(this).parent("ul#sidebarnav").length === 0
//           ? $(this).addClass("active")
//           : $(this).addClass("selected");
//       } else if (!$(this).is("ul") && $(this).children("a").length === 0) {
//         $(this).addClass("selected");
//       } else if ($(this).is("ul")) {
//         $(this).addClass("in");
//       }
//     });
  
//     element.addClass("active");
//     $("#sidebarnav a").on("click", function (e) {
//       if (!$(this).hasClass("active")) {
//         // hide any open menus and remove all other classes
//         $("ul", $(this).parents("ul:first")).removeClass("in");
//         $("a", $(this).parents("ul:first")).removeClass("active");
  
//         // open our new menu and add the open class
//         $(this).next("ul").addClass("in");
//         $(this).addClass("active");
//       } else if ($(this).hasClass("active")) {
//         $(this).removeClass("active");
//         $(this).parents("ul:first").removeClass("active");
//         $(this).next("ul").removeClass("in");
//       }
//     });
//     $("#sidebarnav >li >a.has-arrow").on("click", function (e) {
//       e.preventDefault();
//     });
//   }); 


