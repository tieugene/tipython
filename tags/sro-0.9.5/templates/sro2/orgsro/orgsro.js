$(function() {
    $('#spec').hover(
                    function() {
                        $(this).addClass('ui-state-hover');
                    },
                    function() {
                        $(this).removeClass('ui-state-hover');
                    }
            )
    $('#spec').click(function() {
        $('#speccase').show()
        $('#speccomments').show()
    })
    $('#specedit').click(function() {
        $('#dialog').dialog('open');
    })
    $('#tomembers').click(function() {
        $('#member_dialog').dialog('open');
    })
    $('#tocandidate').click(function() {
        location = "{{ url_for('sro2.views.orgsro_to_candidate', orgsro.id) }}"
    })
    $('#toarchive').click(function() {
        location = "{{ url_for('sro2.views.orgsro_to_archive', orgsro.id) }}"
    })
    $('#returnmember').click(function() {
        location = "{{ url_for('sro2.views.orgsro_return_member', orgsro.id) }}"
    })
    $('#exclude').click(function() {
        $('#exclude_dialog').dialog('open');
    })
    $('#dialog').dialog({
        autoOpen: false,
        title: 'Особый случай',
        modal: true,
        position: 'top',
        width: 600,
        height: 400,
        buttons: {
            "Отмена":function() {
                $('#dialog').dialog('close');
            },
            "Сохранить": function() {
                speccase = '0'
                if ($('#speccasech').attr('checked')) {
                    speccase = '1'
                }
                comment = $('#speccommentsta').val().replace(/\r?\n|\r/g, '<br>');
                specpost = '{"speccase":' + speccase + ',"speccomments":"' + comment + '"}'
                $.post("{{ url_for('sro2.orgsro.views.orgsro_spec_edit', orgsro.id) }}", specpost, function(data) {
                    alert(data)
                    location.reload()
                }, function() {
                    alert('Error!')
                })
            }
        }
    });
    $('#member_dialog').dialog({
        autoOpen: false,
        title: 'Принятие в члены',
        modal: true,
        position: 'top',
        width: 400,
        height: 300,
        buttons: {
            "Отмена":function() {
                $('#member_dialog').dialog('close');
            },
            "Сохранить": function() {
                memberpost = '{"regno":"' + $('#regnoinput').val() + '","regdate":"' + $('#regdateinput').val() + '","protocol":' + $('#member_dialog > p > #id_protocol').val() + '}'
                $.post("{{ url_for('sro2.views.orgsro_to_member', orgsro.id) }}", memberpost, function(data) {
                    alert(data)
                    location.reload()
                }, function() {
                    alert('Error!')
                })
            }
        }
    });
    $('#exclude_dialog').dialog({
        autoOpen: false,
        title: "Исключение из членов",
        modal: true,
        position: 'top',
        width: 600,
        height: 600,
        buttons: {
            "Отмена":function() {
                $('#exclude_dialog').dialog('close');
            },
            "Сохранить": function() {
                var reasons = [];
                $('#reasoninput :checked').each(function() {
                    if ($(this).val() != '' & $(this).val() != 'on') {
                        reasons.push($(this).val());
                    }
                });
                expost = '{"reason":[' + reasons + '],"excludedate":"' + $('#excludedateinput').val() + '","protocol":"' + $('#exclude_dialog > p > #id_protocol').val() + '"}';
                $.post("{{ url_for('sro2.views.orgsro_to_excluded',orgsro.id) }}", expost, function(data) {
                    alert(data)
                    location.reload()
                }, function() {
                    alert('Error!')
                })
            }
        }
    });

    {% if orgsro.speccase == 1 %}
    $('#speccasech').attr('checked', true)
    {% endif %}
})