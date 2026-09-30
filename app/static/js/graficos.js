// Gráficos con Chart.js (incluido en static/vendor/chartjs).
// La plantilla pone en <script id="datos-graficos" type="application/json"> una LISTA de gráficos:
//   [{"id": "id-del-canvas", "tipo": "bar" | "line" | "pie" | "doughnut", "titulo": "...",
//     "formato": "moneda" | "numero" | "porcentaje", "etiquetas": [...], "valores": [...]}]
// Para agregar un gráfico: un <canvas id="..."> en la plantilla y un elemento más en esa lista.
(function () {
    var nodoDatos = document.getElementById("datos-graficos");
    if (!nodoDatos) return;

    // Si Chart.js no cargó por algún motivo, se avisa y quedan las tablas con los mismos datos.
    if (typeof Chart === "undefined") {
        document.querySelectorAll(".grafico").forEach(function (contenedor) {
            contenedor.innerHTML =
                '<p class="texto-suave">No se pudo cargar el gráfico. Los datos están en la tabla.</p>';
            contenedor.style.height = "auto";
        });
        return;
    }

    var formatos = {
        moneda: new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS" }),
        numero: new Intl.NumberFormat("es-AR"),
        porcentaje: new Intl.NumberFormat("es-AR", { maximumFractionDigits: 1 })
    };
    var colorPrimario = getComputedStyle(document.documentElement)
        .getPropertyValue("--color-primario").trim() || "#2563eb";
    var paleta = [colorPrimario, "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2", "#db2777"];

    function formatear(grafico, valor) {
        var formato = formatos[grafico.formato] || formatos.numero;
        return formato.format(valor) + (grafico.formato === "porcentaje" ? " %" : "");
    }

    function crearGrafico(grafico) {
        var canvas = document.getElementById(grafico.id);
        if (!canvas) return;
        var circular = grafico.tipo === "pie" || grafico.tipo === "doughnut";
        new Chart(canvas, {
            type: grafico.tipo,
            data: {
                labels: grafico.etiquetas,
                datasets: [{
                    label: grafico.titulo,
                    data: grafico.valores,
                    backgroundColor: circular ? paleta
                        : grafico.tipo === "line" ? "rgba(37, 99, 235, 0.12)" : colorPrimario,
                    borderColor: circular ? "#ffffff" : colorPrimario,
                    borderWidth: 2,
                    borderRadius: grafico.tipo === "bar" ? 6 : 0,
                    fill: grafico.tipo === "line",
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: circular },
                    tooltip: {
                        callbacks: {
                            label: function (contexto) {
                                return formatear(grafico, circular ? contexto.parsed : contexto.parsed.y);
                            }
                        }
                    }
                },
                scales: circular ? {} : {
                    y: { beginAtZero: true, ticks: { callback: function (valor) { return formatear(grafico, valor); } } }
                }
            }
        });
    }

    JSON.parse(nodoDatos.textContent).forEach(crearGrafico);
})();
