// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        uploading: false,
        upload_done: false,
        profile_picture: "",
    };

    app.load_picture = function () {
        let reader = new FileReader();
        axios.get(profile_pic_url).then(function (response) {
            app.vue.profile_picture = reader.result;
        });

    }

    app.upload_complete = function (filename, filetype) {
        app.vue.uploading = false;
        app.vue.upload_done = true;
        app.vue.uploaded_file = filename;
    }

    app.upload_file = function (event) {
        let input = event.target;
        let file = input.files[0];
        if (file) {
            let reader = new FileReader();
            reader.addEventListener("load", function () {
                axios.post(file_upload_url,
                    {
                        picture: reader.result
                    }).then( function () {
                        app.vue.profile_picture = reader.result;
                    });  
            });
            reader.readAsDataURL(file);
        }
    }

    app.methods = {
        upload_file: app.upload_file,
        load_picture: app.load_picture
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        // Do any initializations (e.g. networks calls) here.
        app.load_picture();
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
