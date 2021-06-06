// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        cart: [],
        total: 0,
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.remove_from_cart = function (_idx) {
        id = app.vue.cart[_idx].id
        axios.get(remove_from_cart_url, {params: {id: id}}).then( function () {
            app.vue.cart.splice(_idx, 1);
        });
    };




    app.methods = {
        remove_from_cart: app.remove_from_cart,

    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });

    app.init = () => {
        // Do any initializations (e.g. networks calls) here.
        axios.get(get_cart_url).then(function (response) {
            merch = response.data.merch;
            app.enumerate(merch);
            app.vue.cart = merch;
            //console.log(merch.length);
            //console.log(merch);
            for (i=0; i<merch.length; i++){
                app.vue.total = app.vue.total + merch[i].item_cost;
                //console.log(merch[i].item_cost);
                //console.log("hello");
            };
            //console.log(app.vue.total);
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
