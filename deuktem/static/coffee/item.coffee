views['item-list'] = ->
    $('#nav-item-list').addClass('active')

    $('.item-list-wish').click ->
        button = $(this)
        itemId = button.data('item-id')
        wished = button.data('wished')
        $.ajax
            type: if not wished then 'POST' else 'DELETE'
            url: 'http://deuktem.joyfl.net/api/items/' + itemId + '/wish'
            dataType: 'json'
            crossDomain: true
            success: (r) ->
                if not wished
                    wishers = $('#item-list-' + itemId + ' .item-list-wishers')
                    label = $('<label />', {
                        id: 'item-' + itemId + '-wisher-' + r['id'],
                        class: 'label label-default',
                        text: r['name']
                    })
                    wishers.append(label)

                    button.data('wished', true)
                    button.text('희망취소')
                    button.removeClass('btn-primary')
                    button.addClass('btn-danger')
                else
                    wisher = $('#item-' + itemId + '-wisher-' + r['id'])
                    wisher.remove()
                    button.data('wished', false)
                    button.text('희망하기')
                    button.removeClass('btn-danger')
                    button.addClass('btn-primary')
            error: (xhr) ->
                return


views['win-list'] = ->
    $('#nav-win-list').addClass('active')


views['item-new'] = ->
    $('#nav-item-new').addClass('active')

    $('#item-new-file').change ->
        preview = $('#item-new-photo')
        if this.files && this.files[0]
            reader = new FileReader()
            reader.readAsDataURL(this.files[0])
            reader.onload = (e) ->
                preview.attr('src', e.target.result)
                preview.css('height', 'auto')

    $('#item-new-form').submit ->
        name = $('#item-new-name')
        description = $('#item-new-description')

        if not name.val()
            error("아이템 이름을 입력해주세요.")
            name.parent().addClass('has-error')
            name.focus()
            return false
        return true

    $('#item-new-name').on 'input', ->
        $(this).parent().removeClass('has-error')

    error = (msg) ->
        errorAlert = $('#item-new-error')
        errorAlert.text(msg)

        if errorAlert.hasClass('hidden')
            errorAlert.removeClass('hidden')
            delay = 1
        else
            errorAlert.removeClass('in')
            delay = 100

        setTimeout((-> errorAlert.addClass('in')), delay)
