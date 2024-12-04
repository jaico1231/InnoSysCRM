document.addEventListener('DOMContentLoaded', function() {
    {% if messages %}
        var messages = [];
        {% for message in messages %}
            messages.push("{{ message|escapejs }}");  // Escapar el mensaje para evitar problemas con comillas
        {% endfor %}
        alert(messages.join("\n"));  // Mostrar todos los mensajes en un alert
    {% endif %}
  });