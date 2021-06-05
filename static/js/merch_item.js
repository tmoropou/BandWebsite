// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        rows: [],
        stars: 5,
        write_review: false,
        review_body: "",
        logged_in: false,
        item: {}
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.toggle_review = function () {
        app.vue.write_review = !app.vue.write_review;
        app.vue.review_body = "";
    }

    app.set_star = function (count) {
        app.vue.stars = count;
    }

    app.load_reviews = function () {
        axios.get(load_reviews_url, {params: {item_id: item.id}}).then(function (response) {
            app.vue.rows = app.enumerate(response.data.rows);
        });
    }

    app.submit_review = function () {
        console.log(app.vue.stars, app.vue.review_body);
        axios.post(add_review_url, {
            body: app.vue.review_body,
            item_id: app.vue.item.id,
            review_score: app.vue.stars,
        }).then(function (response) {
            app.load_reviews();
        })
        app.toggle_review();
    }

    app.check_logged = () => {
        if(global_email != "None"){
            app.vue.logged_in = true;
            return true;
        }
        return false;
    }

    app.add_to_cart = function (id) {
        axios.get(add_to_cart_url, {params: {id: id}}).then( function () {
        });
    };

    app.methods = {
        toggle_review: app.toggle_review,
        set_star: app.set_star,
        submit_review: app.submit_review,
        add_to_cart: app.add_to_cart,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
        // Do any initializations (e.g. networks calls) here.
        app.check_logged();
        app.load_reviews();
        app.vue.item = item;
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
