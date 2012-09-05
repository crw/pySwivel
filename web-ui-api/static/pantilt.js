// Create a YUI instance and request the slider module and its dependencies
YUI().use("slider", "io-base", function (Y) {

var xInput,   // input tied to xSlider
    yInput,   // input tied to ySlider
    xSlider,  // horizontal Slider
    START_VALUE = 90,
    MIN_VALUE = 0,
    MAX_VALUE = 179,
    SLIDER_LENGTH = '180px',
    IO_DELAY = 100,
    state = {
        pan: {
            value: START_VALUE,      // Current pan value 
            time: 0         // Last pan command sent time
        },
        tilt: {
            value: START_VALUE,      // Current tilt value
            time: 0         // Last tilt command sent time
        }
    };

function sendChange(e) {
    var data   = this.getData(),
        slider = data.slider,
        value  = parseInt( this.get( "value" ), 10 ),
        motor  = data.motor,
        now    = (new Date()).getTime(),
        request;

    if (state[motor]) {
        if (state[motor].value != value && 
            now - state[motor].time > IO_DELAY) {                
                console.log(motor + ' to ' + value + ' from ' + state[motor].value);
                state[motor].value = value;
                state[motor].time = now;
                request = Y.io('/' + motor + '/' + value, {
                    method: 'PUT'
                });
        }
    }
}

// Function to pass input value back to the Slider
function updateSlider(e) {
    var data   = this.getData(),
        slider = data.slider,
        value  = parseInt(this.get("value"), 10 );

    if ( data.wait ) {
        data.wait.cancel();
    }

    // Update the Slider on a delay to allow time for typing
    data.wait = Y.later( 500, slider, function () {
        data.wait = null;
        this.set( "value", value );
    } );
}

// Function to update the input value from the Slider value
function updateInput( e ) {
    this.set("value", e.newVal);
}

// Create the vertical Slider.
xInput = Y.one("#horiz_value");
xInput.setData("slider", new Y.Slider({
            axis: 'x',
            min   : MIN_VALUE,      // min is the value at the top
            max   : MAX_VALUE,     // max is the value at the bottom
            value : START_VALUE,       // initial value
            length: SLIDER_LENGTH,  // rail extended to afford all values
            // construction-time event subscription
            after : {
                valueChange: Y.bind(updateInput, xInput),
            }
        }).render('.horiz_slider')
    )
    .setData('motor', 'pan')
    .on('keyup', updateSlider);
xInput.getData('slider').on('valueChange', Y.bind(sendChange, xInput));
    
// Create the vertical Slider.
yInput = Y.one("#vert_value");
yInput.setData("slider", new Y.Slider({
            axis: 'y',
            min   : MIN_VALUE,      // min is the value at the top
            max   : MAX_VALUE,     // max is the value at the bottom
            value : START_VALUE,       // initial value
            length: SLIDER_LENGTH,  // rail extended to afford all values

            // construction-time event subscription
            after : {
                valueChange: Y.bind(updateInput, yInput)
            }
        }).render(".vert_slider") // render returns the Slider
    )                               // set( "data", ... ) returns the Node
    .setData('motor', 'tilt')
    .on("keyup", updateSlider);   // chain the keyup subscription
yInput.getData('slider').on("valueChange", Y.bind(sendChange, yInput));
});