function loadModalAndHandleForm(btn, url) {
    var contratoId = btn.getAttribute('data-id');
    var modalBody = document.querySelector('#editModal .modal-body');
    modalBody.innerHTML = '<p>Cargando...</p>';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url.replace('0', contratoId));
    xhr.onload = function() {
        if (xhr.status === 200) {
            modalBody.innerHTML = xhr.responseText;
            $('#editModal').modal('show');

            var form = modalBody.querySelector('form');
            form.addEventListener('submit', function(event) {
                event.preventDefault();

                var formData = new FormData(form);
                var saveXhr = new XMLHttpRequest();
                saveXhr.open('POST', url.replace('0', contratoId));
                saveXhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value); // Asegúrate de pasar el CSRF token correctamente
                saveXhr.onload = function() {
                    if (saveXhr.status === 200) {
                        try {
                            var response = JSON.parse(saveXhr.responseText);
                            
                            if (response.success) {
                                $('#editModal').modal('hide');
                                // updateContractList(); //esto no se que hace
                            } else {
                                modalBody.innerHTML = saveXhr.responseText;
                                location.reload();
                            }
                        } catch (e) {
                            modalBody.innerHTML = saveXhr.responseText;
                            location.reload();
                        }
                    } else {
                        modalBody.innerHTML = '<p>Error al guardar la información.</p>';
                        location.reload();
                    }
                };
                saveXhr.send(formData);
            });
        } else {
            modalBody.innerHTML = '<p>Error al cargar la vista.</p>';
            location.reload();
        }
    };
    xhr.send();
}
