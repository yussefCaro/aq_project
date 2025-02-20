document.addEventListener("DOMContentLoaded", function () {
    let container = document.getElementById("fecha_form_container");
    let emptyFormElement = document.getElementById("empty-form");
    let totalForms = document.querySelector("#id_fechaetapa2_set-TOTAL_FORMS");

    console.log("Container:", container);
    console.log("Empty Form:", emptyFormElement);
    console.log("Total Forms:", totalForms);

    if (!emptyFormElement) {
        console.error("Error: No se encontró el elemento con ID 'empty-form'");
        return;
    }
    if (!totalForms) {
        console.error("Error: No se encontró el elemento con ID 'id_fechaetapa2_set-TOTAL_FORMS'");
        return;
    }

    let emptyForm = emptyFormElement.innerHTML;

    document.getElementById("agregar_fecha_etapa2").addEventListener("click", function () {
        let newForm = document.createElement("div");
        newForm.innerHTML = emptyForm.replace(/__prefix__/g, totalForms.value);
        newForm.classList.add("fecha_etapa2", "mb-3");
        container.appendChild(newForm);

        totalForms.value = parseInt(totalForms.value) + 1;
    });

    container.addEventListener("click", function (event) {
        if (event.target.classList.contains("eliminar_fecha")) {
            event.target.closest(".fecha_etapa2").remove();
            totalForms.value = parseInt(totalForms.value) - 1;
        }
    });
});
