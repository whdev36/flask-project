$(document).ready(() => {
    $('.delete-note').on('click', function () {
        const noteId = $(this).closest('li').data('id');

        $.ajax({
            url: '/delete-note',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ noteId: noteId }),
            success: function () {
                $(`li[data-id='${noteId}']`).remove();
            },
            error: function (xhr, status, error) {
                console.error("Error deleting note:", error);
            }
        });
    });
});
