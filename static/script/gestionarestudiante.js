$(document).ready(function () {
     const fvNuevoEstudiante = formNewStudent();
});

function formNewStudent() {
    const fvNuevoEstudiante = document.getElementById('fnuevoestudiante');
    const fv = FormValidation.formValidation(fconsejeria, {
        plugins: {
            trigger: new FormValidation.plugins.Trigger(),
            bootstrap: new FormValidation.plugins.Bootstrap(),
            submitButton: new FormValidation.plugins.SubmitButton(),
        },
        fields: {
            'name_student': {
                validators: {
                    regexp: {
                        regexp: /^[ A-Za-z0-9ñÑáéíóúÁÉÍÓÚ#().:,;%_-]+$/,
                        message: ErrRegexpMsg
                    },
                    notEmpty: {
                        message: ErrNotEmptyMsg
                    }
                }
            },
            'last_name_p_student': {
                validators: {
                    regexp: {
                        regexp: /^[ A-Za-z0-9ñÑáéíóúÁÉÍÓÚ#().:,;%_-]+$/,
                        message: ErrRegexpMsg
                    },
                    notEmpty: {
                        message: ErrNotEmptyMsg
                    }
                }
            },
            'last_name_m_student': {
                validators: {
                    regexp: {
                        regexp: /^[ A-Za-z0-9ñÑáéíóúÁÉÍÓÚ#().:,;%_-]+$/,
                        message: ErrRegexpMsg
                    },
                    notEmpty: {
                        message: ErrNotEmptyMsg
                    }
                }
            },
            'edad_estudiante': {
                validators: {
                    regexp: {
                        regexp: /^[ A-Za-z0-9ñÑáéíóúÁÉÍÓÚ#().:,;%_-]+$/,
                        message: ErrRegexpMsg
                    },
                    notEmpty: {
                        message: ErrNotEmptyMsg
                    }
                }
            },
            'email_estudiante': {
                validators: {
                    regexp: {
                        regexp:  /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/,
                        message: ErrRegexpMsg
                    },
                    notEmpty: {
                        message: ErrNotEmptyMsg
                    }
                }
            },
         
        }
    })
        .on('core.element.validated', function(e){
            if (e.valid){
                // Remove is-valid from the element
                FormValidation.utils.classSet(e.element, {'is-valid': false,});
            }
        });

    return fv;
}