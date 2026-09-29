// Gráficos de la página de estadísticas (usa Chart.js, incluido en static/vendor/chartjs).
// Los datos los pone el servidor en <script id="datos-graficos" type="application/json">.
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

    var datos = JSON.parse(nodoDatos.textContent);
    var moneda = new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS" });
    var colorPrimario = getComputedStyle(document.documentElement)
        .getPropertyValue("--color-primario").trim() || "#2563eb";

    function crearGrafico(idCanvas, tipo, serie) {
        var canvas = document.getElementById(idCanvas);
        if (!canvas) return;
        new Chart(canvas, {
            type: tipo,
            data: {
                labels: serie.etiquetas,
                datasets: [{
                    label: "Facturación",
                    data: serie.valores,
                    backgroundColor: tipo === "line" ? "rgba(37, 99, 235, 0.12)" : colorPrimario,
                    borderColor: colorPrimario,
                    borderWidth: 2,
                    borderRadius: 6,
                    fill: tipo === "line",
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (contexto) { return moneda.format(contexto.parsed.y); }
                        }
                    }
                },
                scales: {
                    y: { beginAtZero: true, ticks: { callback: function (valor) { return moneda.format(valor); } } }
                }
            }
        });
    }

    crearGrafico("grafico-categorias", "bar", datos.categorias);
    crearGrafico("grafico-meses", "line", datos.meses);
})();
