$(function() {

    var prevdate = $.datepicker.parseDate('dd.mm.yy', "{{prevdate}}");
    mindate = new Date(prevdate);
    mindate.setDate(prevdate.getDate() + 1);

    $('#pausePermit').click(function(index) {
        $('#dialog_pause').dialog('open');
    });

    $('#resumePermit').click(function(index) {
        $('#dialog_resume').dialog('open');
    });
    {% if stagelist.isperm() %}
    $('#dialog_pause').dialog({
        autoOpen: false,
        title: 'Приостановка свидетельства',
        modal: true,
        position: 'top',
        width: 600,
        height: 340,
        buttons: {
            "Отмена":function() {
                $('#dialog_pause').dialog('close');
            },
            "Приостановить свидетельство": function() {
                var datesince = $.datepicker.parseDate('dd.mm.yy', $('#datesince_pause').val());
                datesince = new Date(datesince);
                var datetill = $.datepicker.parseDate('dd.mm.yy', $('#datetill').val());
                datetill = new Date(datetill);
                if ($('#dialog_pause #id_protocol').val() && datesince >= mindate && datetill > datesince) {
                    post = '{"protocol":"' + $('#dialog_pause #id_protocol').val() + '", "datesince":"' + $('#datesince_pause').val() + '", "datetill":"' + $('#datetill').val() + '"}'
                    $.post(
                            "{{ url_for('sro2.views.permit_pause_allstages', prevpermit_id) }}",
                            post,
                          function(data) {
                              location.reload()
                          }
                            );
                    $('#dialog_pause').dialog('close');
                } else {
                    alert('Для приостановки необходимо выбрать протокол и дату из допустимого диапазона!')
                }
            },
        },
    });

    $('#dialog_resume').dialog({
        autoOpen: false,
        title: 'Возобновление свидетельства',
        modal: true,
        position: 'top',
        width: 600,
        height: 340,
        buttons: {
            "Отмена":function() {
                $('#dialog_resume').dialog('close');
            },
            "Возобновить свидетельство": function() {
                var datesince = $.datepicker.parseDate('dd.mm.yy', $('#datesince_resume').val());
                datesince = new Date(datesince);
                if ($('#dialog_resume #id_protocol').val() && datesince >= mindate) {
                    post = '{"protocol":"' + $('#dialog_resume #id_protocol').val() + '", "datesince":"' + $('#datesince_resume').val() + '"}'
                    $.post(
                            "{{ url_for('sro2.views.permit_resume_allstages', prevpermit_id) }}",
                            post,
                          function(data) {
                              location.reload()
                          }
                            );
                    $('#dialog_resume').dialog('close');
                } else {
                    alert('Для возобновления необходимо выбрать протокол и дату из допустимого диапазона!')
                }
            },
        },
    });
    $('.ui-dialog-titlebar-close').hide()
        {%endif%}


    function setdate(datasince, delta) {
        var datasince = $.datepicker.parseDate('dd.mm.yy', datasince);
        datatill = new Date(datasince);
        datatill.setDate(datasince.getDate() + parseInt(delta))
        day = datatill.getDate()
        month = datatill.getMonth() + 1
        year = datatill.getFullYear()
        $('#datetill').val(day + '.' + month + '.' + year)
    }

    $('#delta').change(function() {
        setdate($('#datesince_pause').val(), $('#delta').val())
    })

    $('#datesince_pause').change(function() {
        setdate($('#datesince_pause').val(), $('#delta').val())
    })

    $('#datesince_pause, #datesince_resume').datepicker({dateFormat: 'dd.mm.yy', changeMonth: true, minDate: mindate }).datepicker($.datepicker.regional['ru']);
});


