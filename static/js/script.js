//<reference path="../../typings/globals/jquery/index.d.ts" />

$(document).ready(function () {
    $('#inputCepFrete').mask('00.000-000');
    $("#id_password").addClass("form-control")
    $('#id_password').attr('placeholder', 'Senha');
    $('#id_username').attr('placeholder', 'Usuário');
    $("#id_username").addClass("form-control")

    // $('#dropdownCategoria').hover(function () {
    //     $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(500);//strop(clearQueue, jumpToEnd)
    // }, function () {
    //     $(this).find('.dropdown-menu').stop(true, true).delay(80).fadeOut(500);
    // });
    
    var step = parseFloat($('#quantidade').attr('data-step').replace(",",'.'));
    $('.diminuiQuantidade').click(function (e) {
        qVar = parseFloat($('#quantidade').val().replace(",","."));
        console.log(qVar)
        console.log(step)
        resultado = Math.round((qVar - step)*100)/100
        if (qVar > step) {
            $('#quantidade').val((resultado+"").replace(".",","));
        }
    });

    $('.aumentaQuantidade').click(function (e) {
        qVar = parseFloat($('#quantidade').val().replace(",","."));
        console.log(qVar)
        console.log(step)
        // console.log(quantity + step)
        resultado = Math.round((qVar + step)*100)/100
        resultado = resultado.toFixed(2)
        if (qVar < 9999) {
            $('#quantidade').val((resultado+"").replace(".",","));
        }
    });
});


$(function () {

    $('.carousel').carousel({
        interval: 4000
    });

    $('.toast').toast('show');

    $('.alert').alert();

    $('.tooltip').tooltip();

    
});
   
$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
    if (!$(this).next().hasClass('show')) {
        $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
    }
    var $subMenu = $(this).next('.dropdown-menu');
    $subMenu.toggleClass('show');

    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
        $('.dropdown-submenu .show').removeClass('show');
    });

    return false;
});