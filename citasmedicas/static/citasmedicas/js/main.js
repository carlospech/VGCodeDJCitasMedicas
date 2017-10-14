window.onload = function() {
    Vue.config.delimiters = ["[[", "]]"]
    Vue.http.headers.common['X-CSRFToken'] = $("[name=csrfmiddlewaretoken]").val();
    var demo = new Vue({
        el: '#editor',
        data: {
            'apptitle': 'Django vue',
            'doctores': []
        },
        methods: {
            addDoctor: function() {
                var newDoctor = {
                    usuario: this.usuario,
                    nombres: this.nombres.trim(),
                    apellido_paterno: this.apellido_paterno.trim(),
                    apellido_materno: this.apellido_materno.trim(),
                    titulo: this.titulo.trim(),
                    especialidad: this.especialidad.trim(),
                    cedula_profesional: this.cedula_profesional.trim(),
                    cedula_especialidad: this.cedula_especialidad.trim(),
                    registro_ssa: this.registro_ssa.trim()
                };
                this.$http.post('http://127.0.0.1:8000/citasmedicas/doctores/', newDoctor).then(response => {
                  this.$http.get('http://127.0.0.1:8000/citasmedicas/doctores/').then(function(response) {
                      this.doctores = response.data;
                  }, function(response) {
                      console.log(response);
                  });
                  $('input').val('');
                }, response => {
                    console.log(response);
                });
            },
            removeDoctor: function(index) {
                this.$http.delete('http://127.0.0.1:8000/citasmedicas/doctores/'.concat(this.doctores[index].id)).then(function(response) {
                  this.$http.get('http://127.0.0.1:8000/citasmedicas/doctores/').then(function(response) {
                      this.doctores = response.data;
                  }, function(response) {
                      console.log(response);
                  });
                }, function(response) {
                    console.log(response);
                });
            }
        },
        ready: function() {
            this.$http.get('http://127.0.0.1:8000/citasmedicas/doctores/').then(function(response) {
                this.doctores = response.data;
            }, function(response) {
                console.log(response);
            });
        }
    });
}
