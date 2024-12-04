function abrir_modal_edicion(url){
    // $('#detalles').load(url, function(){
    //      myModal.show();
    //  });
     alert(url);
 };
//codigo para el cuadro de carga de imagen 
const fileInput = document.getElementById('id_imagen')
const dragZone = document.getElementById('result-imagen')
const img = document.getElementById('img-result')

dragZone.addEventListener('click', () =>  fileInput.click() )
dragZone.addEventListener('dragover', (e) => {
  e.preventDefault()
  dragZone.classList.add('form-file__result--active')
})
dragZone.addEventListener('dragleave', (e) => {
  e.preventDefault()
  dragZone.classList.remove('form-file__result--active')
})
const uploadImage = (file) => {
  const fileReader = new FileReader()
  fileReader.readAsDataURL(file)
  fileReader.addEventListener('load', (e) => {
    img.setAttribute('src', e.target.result)
  }) 
}

dragZone.addEventListener('drop', (e) => {
  e.preventDefault()

  dragZone.classList.remove('form-file__result--active')
  fileInput.files = e.dataTransfer.files
  const file = fileInput.files[0]
  uploadImage(file)
})

function DataTable_Script() {
    var table = new DataTable('#data', {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-CO.json',
        },
    });
    var table = new DataTable('#data1', {
      language: {
          url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-CO.json',
      },
  });
  var table = new DataTable('#data2', {
    language: {
        url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-CO.json',
    },
});
var table = new DataTable('#data3', {
  language: {
      url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-CO.json',
  },
});
var table = new DataTable('#data4', {
  language: {
      url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-CO.json',
  },
});
var table = new DataTable('#data5', {
  language: {
      url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-CO.json',
  },
});
}
//Converir numeros a letras
function numberToWords(num) {
  if (num === 0) {
      return 'cero';
  }

  var ones = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'];
  var teens = ['diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve'];
  var tens = ['', '', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa'];
  var thousands = ['', 'mil', 'millones', 'mil millones', 'mil millones de millones', 'mil millones de mil millones', 'mil millones de mil millones de millones'];

  if (num < 10) {
      return ones[num];
  } else if (num < 20) {
      return teens[num - 10];
  } else if (num < 100) {
      return tens[Math.floor(num / 10)] + (num % 10 === 0 ? '' : ' ' + ones[num % 10]);
  } else if (num < 1000) {
      return ones[Math.floor(num / 100)] + ' cientos' + (num % 100 === 0 ? '' : ' ' + numberToWords(num % 100));
  } else if (num < 1000000) {
      return numberToWords(Math.floor(num / 1000)) + ' mil' + (num % 1000 === 0 ? '' : ' ' + numberToWords(num % 1000));
  } else if (num < 1000000000) {
      return numberToWords(Math.floor(num / 1000000)) + ' millones' + (num % 1000000 === 0 ? '' : ' ' + numberToWords(num % 1000000));
  } else {
      return numberToWords(Math.floor(num / 1000000000)) + ' mil millones' + (num % 1000000000 === 0 ? '' : ' ' + numberToWords(num % 1000000000));
  }
}
// Codigo para seleccionar paises departamentos municipios y barrios de manera dinamica


function select_paises() {
  document.addEventListener('DOMContentLoaded', function() {
      const paisSelect = document.getElementById('paises');
      const departamentoSelect = document.getElementById('departamentos');
      const municipioSelect = document.getElementById('municipios');
    
      paisSelect.addEventListener('change', function() {
        const selectedPais = paisSelect.value;
        // Realizar una solicitud AJAX para obtener los departamentos del país seleccionado
        fetch(`/obtener_departamentos?id_pais=${selectedPais}`)
          .then(response => response.json())
          .then(data => {
            departamentoSelect.innerHTML = '<option value="">Seleccionar departamento</option>';
            data.forEach(departamento => {
              const option = document.createElement('option');
              option.value = departamento.id;
              option.textContent = departamento.departamento;
              departamentoSelect.appendChild(option);
            });
            departamentoSelect.disabled = false;
          });
      });
    
      departamentoSelect.addEventListener('change', function() {
        const selectedDepartamento = departamentoSelect.value;
        // Realizar una solicitud AJAX para obtener los municipios del departamento seleccionado
        fetch(`/obtener_municipios?id_departamento=${selectedDepartamento}`)
          .then(response => response.json())
          .then(data => {
            municipioSelect.innerHTML = '<option value="">Seleccionar municipio</option>';
            data.forEach(municipio => {
              const option = document.createElement('option');
              option.value = municipio.id;
              option.textContent = municipio.municipio;
              municipioSelect.appendChild(option);
            });
            municipioSelect.disabled = false;
          });
      });
    });
  
}