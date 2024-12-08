// let fecha = hoy.toDateString();
// const header = `<p style="margin-top: 50px align: right">
//    Acopi Yumbo, Valle del Cauca CO, ${fecha}
// </p>`
let hoy = new Date();
let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
let fecha = hoy.toLocaleDateString('es-ES', options);

const header = `<p style="margin-top: 50px; text-align: right;">
   Acopi Yumbo, Valle del Cauca CO, ${fecha}
</p>`;

function getHtml(data, option) {
    const datos = JSON.parse(data)[0]
    console.log(datos, option)

const options = {
        4: `<div style="padding: 30px; height: 100%;">
        <p>Señores.<br>
            BANCO AV VILLAS S.A.<br>
            NIT. 860.035.827-5.</p>
            
            <p style="text-align: center;">ASUNTO: CERTIFICACIÓN DE APERTURA CUENTA DE NOMINA AV VILLAS.</p>
            
            <p>Por medio de la presente se solicita realizar la apertura de cuenta de nómina al señor(a) relacionado(a) a continuación, adicionalmente su asociación a la cuenta matriz de la empresa,</p>
            
            <p style="text-align: center;">
            <b>Datos de Empresa:</b><br>
            </p>
            <p>
            Tipo y Número de Identificación	NIT. 805.001.883-1<br>
            Razón Social	INDUSTRIAS ROMIL S.A.S.<br>
            No. Cuenta Matriz	131-23391-8</p>
            
            <p style="text-align: justify;">Datos de Empleado:<br>
            <b>Tipo y Número de Identificación</b>	${datos.fields?.tipo_documentoFK} DE ${datos.fields?.lugar_expedicion}, (DEPARTAMENTO) CO<br>
            Nombres y Apellidos	NOMBRE DE LA PERSONA<br>
            Fecha Ingreso a Empresa	XX DE (MES EN LETRA. EJ.: ENERO) DE 2.02X<br>
            Salario Base	$XXXXX<br>
            Tipo Contrato, Cargo	FIJO INFERIOR A UN AÑO, (CARGO DE LA PERSONA)</p>
            
            <p>La actual debe constar de firmas reconocidas por el banco y sellos correspondientes (maquina proyectora 1,2,3,4,5,6,7,8,9,00 y el sello húmedo en la parte inferior).<br>
            Se certifica veracidad y confiabilidad de la información suscrita en la presente a los (Cantidad de días en letras) (#) días del mes de XXX del año dos mil veintixxx (202x).</p>
            
            <p>Cordialmente,</p>
        
        </div>`,
        8: `<div style="padding: 30px; height: 100%;">
${header}

<p>Señor(a).</p>

<b style="text-transform: uppercase, text-align: justify;">${datos.fields.nombre} ${datos.fields.apellido}</b>
<br>
${datos.fields?.tipo_documentoFK} ${datos.fields?.numero_identificacion}
<br>
<br>
<br>
<b>
    ASUNTO: LLAMADO DE ATENCIÓN.
</b>
<hr>

Apreciado(a) Sr(a). ${ datos.fields.nombre } ${ datos.fields.apellido }.
Reciba un cordial saludo,

Una vez agotado el procedimiento del Art. 115 del CST mediante la diligencia de descargos llevada a cabo el día (#Dia)
de (Mes en letra. Ej.: Enero) de 2.02x, en la cual quedo clara su responsabilidad sobre (Descripción Acción Irregular
Cometida); <b>INDUSTRIAS ROMIL S.A.S</b>, ha tomado la decisión de hacerle un <b>LLAMADO DE ATENCION</b>, con el único propósito de
que en lo sucesivo no se presente(n) el(los) hecho(s) ocurrido el día (#Dia) de (Mes en letra. Ej.: Enero) de 2.02x.
Estamos totalmente seguros de que contamos con su compromiso para con la empresa siendo conocedores de su don de gentes,
su capacidad de trabajo y profesionalismo.
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
Cordialmente,
</div>
`
}

    return options[option]
}
