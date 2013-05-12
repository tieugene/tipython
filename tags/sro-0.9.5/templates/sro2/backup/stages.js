/* Не исрользуется. Приостановка и возобновление выбоанных работ */

$(function() {
    $("#cancelSort").click(function() {
        $("#sortable1, #sortable2").sortable("cancel");
    });

    $('#dialog_resume').dialog({
        autoOpen: false,
        title: 'Возобновление',
        modal: true,
        position: 'top',
        width: 600,
        height: 400,
        buttons: {
            "Отмена":function() {
                $('#dialog_resume').dialog('close');
            },
            "Сохранить": function() {
                if ($('#dialog_resume #id_protocol').val()) {
                    paused = []
                    active = []
                    $('#sortable2 li:not([class~=listheader]):not([class~=parentstage])').each(function() {
                        paused.push('{"id":' + $(this).attr('id') + ',"date":"' + $('#datedue').val() + '"}')
                    })
                    $('#sortable1 li:not([class~=listheader])').each(function() {
                        active.push('{"id":' + $(this).attr('id') + '}')
                    })
                    stages = '{"active":[' + active + '],"paused":[' + paused + '],"protocol":"' + $('#dialog_resume #id_protocol').val() + '","datesince":"' + $('#datetill').val() + '"}'
                    $.post("{% url sro2.views.permit_pause prevpermit_id danger %}", stages, function(data) {
                        location = '{% url sro2.views.orgsro_view stagelist.orgsro.id %}#permit'
                    }, function() {
                        alert('Error!')
                    })
                    /*$('#datedue').val('')*/
                    $('#dialog').dialog('close');
                    var stages = []
                } else {
                    alert('Выберите протокол.')
                }

            },
        },
    });


    $('#dialog').dialog({
        autoOpen: false,
        title: 'Приостановка',
        modal: true,
        position: 'top',
        width: 600,
        height: 420,
        buttons: {
            "Отмена":function() {
                $('#dialog').dialog('close');
                $("#sortable1, #sortable2").sortable("cancel");
            },
            "Приостановить работы": function() {
                if ($('#dialog #id_protocol').val()) {
                    paused = []
                    active = []
                    $('#sortable2 li:not([class~=listheader]):not([class~=parentstage])').each(function() {
                        paused.push('{"id":' + $(this).attr('id') + ',"date":"' + $('#datedue').val() + '"}')
                    })
                    $('#sortable1 li:not([class~=listheader])').each(function() {
                        active.push('{"id":' + $(this).attr('id') + '}')
                    })
                    stages = '{"active":[' + active + '],"paused":[' + paused + '],"protocol":"' + $('#dialog #id_protocol').val() + '","datesince":"' + $('#datetill').val() + '"}'
                    $.post("{% url sro2.views.permit_pause prevpermit_id danger %}", stages, function(data) {
                        location = '{% url sro2.views.orgsro_view stagelist.orgsro.id %}#permit'
                    }, function() {
                        alert('Error!')
                    })
                    /*$('#datedue').val('')*/
                    $('#dialog').dialog('close');
                    var stages = []
                } else {
                    alert('Выберите протокол.')
                }

            },
        },
    });
    $('#applyChanges').click(function(index) {
        if ($('li[mod="true"]').length != 0) {
            if ($('#sortable2 > li[mod="true"]').length != 0) {
                $('#dialog').dialog('open');
            } else {
                $('#dialog_resume').dialog('open');

            }
        } else {
            alert('Нет изменений для применения.')
        }
    })

    $('#clearSearch').click(function() {
        $('input#id_search_list').val('')
        $(':not(li[class~=listheader])').removeClass('ui-state-disabled')
    })

    $('.ui-dialog-titlebar-close').hide()
    $('input#id_search_list').quicksearch('ul#sortable1 li:not([class~=listheader]), ul#sortable2 li:not([class~=listheader])');

    $("#maincheck").click(function() {
        $('.mc').attr('checked', $('#maincheck').attr('checked'));
    });

    $("#maincheck2").click(function() {
        $('.mc2').attr('checked', $('#maincheck2').attr('checked'));
    });

    $('.mc, .mc2').change(function() {
        cbSelect = '.stage[parent=' + $(this).parent().attr('id') + '] input' + '.' + $(this).attr('class')
        thisState = $(this).attr('checked')
        $(cbSelect).attr('checked', thisState);
        $(cbSelect).each(function(index, thisState) {
            cbSelect2 = '.stage[parent=' + $(this).parent().attr('id') + '] input'
            $(cbSelect2).attr('checked', $(this).attr('checked'));
        })
    })

    $('#activecount').html('[' + $("ul#sortable1 > li:not([class~=ui-state-disabled])").length + ']');
    $('#pausedcount').html('[' + $("ul#sortable2 > li:not([class~=ui-state-disabled])").length + ']');
    if ($("ul#sortable1 > li:not([class~=ui-state-disabled])").length == 0) {
        $('#stopSelected').hide()
    }
    if ($("ul#sortable2 > li:not([class~=ui-state-disabled])").length == 0) {
        $('#resumeSelected').hide()
    }
    function setdate(start, delta) {
        //alert(start)
        if (start) {
            var instance = $(this).data("datepicker");
            var date = $.datepicker.parseDate('dd.mm.yy', start);
            //alert(date)
            today = new Date;
            today.setDate(date.getDate() + parseInt(delta))
            month = today.getMonth() + 1
            day = today.getDate()
            year = today.getFullYear()
        }
        else {

            today = new Date;
            today.setDate(today.getDate() + parseInt(delta))
            month = today.getMonth() + 1
            day = today.getDate()
            year = today.getFullYear()

        }
        $('#datedue').val(day + '.' + month + '.' + year)
        //alert(day+'.'+month+'.'+year)
    }

    //setdate(60)
    function get_selected(class) {
        var stages = [];
        $(class + ':checked').each(function() {
            if ($(this).val() != '' && $(this).attr('cat') != 'true') {
                stages.push($(this).val());
            }
        });
        return stages;
    }

    $('#delta').change(function() {
        setdate($('#datetill').val(), $('#delta').val())
    })
    $('#datetill').change(function() {
        setdate($('#datetill').val(), $('#delta').val())
    })
    $('#stopSelected').click(function() {
        stages = get_selected('#sortable1 .mc')
        if (stages.length > 0) {
            var codes = [];
            $.each(stages, function(i, val) {
                codes.push($('#' + val).attr('code'))
            })
            //$('#stagetitle').html(codes.join(','))
            //$('#stagetitle').attr('sids',stages)
            stages = get_selected('.mc')
            $.each(stages, function(i, val) {
                if (val) {
                    item = $('li[id=' + val + ']')
                    //item.attr('date',$('#datedue').val())
                    //item.append('<span id="inlinedate">[Приостановлен до: <span style="color: red;"><b>'+$('#datedue').val()+'</b></span>]</span>')
                    item.appendTo('#sortable2')
                    item.attr('mod', 'true')
                }
            })
            $('.mc').attr('checked', false)
        } else {
            alert('Выберите хотя бы одну работу')
        }
    });

    $('#resumeSelected').click(function() {
        stages = get_selected('#sortable2 .mc2')
        if (stages.length > 0) {
            var codes = [];
            $.each(stages, function(i, val) {
                $('li[id=' + val + ']').attr('mod', 'true')
                $('li[id=' + val + ']').children('#inlinedate').html('[<span style="color: #0078ae;"><b>Поставлен на возобновление</b></span>]')
                $('li[id=' + val + ']').appendTo('#sortable1')
                $('.mc2').attr('checked', false)
                //codes.push($('#'+val).attr('code'))
            })
        } else {
            alert('Выберите хотя бы одну работу')
            //$('#stagetitle').html(codes.join(','))
            //$('#stagetitle').attr('sids',stages)
            //$('#dialog').dialog('open');
        }
    });


    /*end*/
});

