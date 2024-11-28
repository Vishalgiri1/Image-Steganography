


let encodebtn = document.getElementById("encodebtn")
let encodeimage1fileinput = document.getElementById("encodeimage1")



let secretTextField = document.getElementById("secretText");
let secretTextField1 = document.getElementById("secretText1");

let loadedImage;
let encodedImage;

let decodebtn = document.getElementById("decodebtn")
let decodeimage1fileinput = document.getElementById("decodeimage1")
let decodeimage2fileinput = document.getElementById("decodeimage2")



// SYNTAX TO DISPLAY SELECTED IMAGE ON SCREEN

const encodeimage1 = document.querySelector("#encodeimage1");
let uploadedImage = "";

encodeimage1.addEventListener("change",function(){
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        uploadedImage = reader.result;
        document.querySelector("#image-display").style.backgroundImage=`url(${uploadedImage})`
    } )
    reader.readAsDataURL(this.files[0])
})

const decodeimage1 = document.querySelector("#decodeimage1");
let uploadedImage1 = "";

decodeimage1.addEventListener("change",function(){
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        uploadedImage1 = reader.result;
        document.querySelector("#image-display-Original").style.backgroundImage=`url(${uploadedImage1})`
    } )
    reader.readAsDataURL(this.files[0])
})

const decodeimage2 = document.querySelector("#decodeimage2");
let uploadedImage2 = "";

decodeimage2.addEventListener("change",function(){
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        uploadedImage2 = reader.result;
        document.querySelector("#image-display-Encoded").style.backgroundImage=`url(${uploadedImage2})`
    } )
    reader.readAsDataURL(this.files[0])
})

// ENCODE THE IMAGE

encodebtn.addEventListener("click", e => {
    console.log("encoding...")
    encodebtn.classList.add("disbaled")
    // load image from encodeimage1fileinput and display in canvasbox
    // Check if a file is selected
    if (encodeimage1fileinput.files && encodeimage1fileinput.files[0]) {
        
        loadedImage = loadImage(URL.createObjectURL(encodeimage1fileinput.files[0]), () => {
            // Draw the loaded image to the canvasbox div
            loadedImage.loadPixels();
            console.log("Pixel data:", loadedImage.pixels);

            //  text to hide
            let secretText = secretTextField.value;
            console.log("secret message:", secretText)

            // Encode the message in the image
            encodedImage = createImage(loadedImage.width, loadedImage.height);
            encodedImage.copy(loadedImage, 0, 0, loadedImage.width, loadedImage.height, 0, 0, loadedImage.width, loadedImage.height);

            encodedImage.loadPixels()
            console.log("Pixel data:", encodedImage.pixels);

            // Encode the message in the image
            encodeMessage(encodedImage, secretText);

            // Auto download the encodedimage

            downloadEncodedImage(encodedImage, 'encoded_image.jpg');


        });
    } else {
        alert("Please select an image file.");
    }
})

decodebtn.addEventListener("click", e => {
    console.log("decoding...")
    decodebtn.classList.add("disbaled")


    //load images - first one is original and second one with message. compare them and find the message inside
    // Check if both files are selected
    if (decodeimage1fileinput.files && decodeimage1fileinput.files[0] && decodeimage2fileinput.files && decodeimage2fileinput.files[0]) {
        // Load the two images
        loadImage(URL.createObjectURL(decodeimage1fileinput.files[0]), img1 => {
            loadImage(URL.createObjectURL(decodeimage2fileinput.files[0]), img2 => {
                

                img1.loadPixels()
                img2.loadPixels()
                console.log("image 1:", img1)
                console.log("image 2:", img2)

                // Decode the hidden message
                let decodedMessage = decodeMessage(img1, img2);
                console.log("Decoded Message:", decodedMessage);


                // Enable the decode button after decoding
                //    decodebtn.classList.remove("disabled");


                secretTextField1.value = decodedMessage

            });
        });
    } else {
        alert("Please select both image files.");
    }

})


// Define the p5.js sketch
function setup() {
}


function draw() {
    noLoop()
}

// Function to encode the message by modifying color channels
function encodeMessage(img, message) {
    let binaryMessage = textToBinary(message);
    img.loadPixels();

    let index = 0;
    for (let i = 0; i < img.pixels.length; i += 4) {
        for (let j = 0; j < 3; j++) {
            if (index < binaryMessage.length) {
                // Get the binary value from the message
                let bit = int(binaryMessage[index]);

                // Only increment the color channel value if the bit is 1 and the current value is not at the maximum (255)
                if (bit === 1 && img.pixels[i + j] < 255) {
                    img.pixels[i + j]++;
                } else if (bit === 1 && img.pixels[i + j] == 255) {
                    img.pixels[i + j]--;

                }

                index++;
            }
        }
    }

    img.updatePixels();
}



function textToBinary(text) {
    let binaryMessage = '';
    for (let i = 0; i < text.length; i++) {
        let binaryChar = text[i].charCodeAt(0).toString(2);
        binaryMessage += '0'.repeat(8 - binaryChar.length) + binaryChar;
    }
    return binaryMessage;
}


function downloadEncodedImage(img, filename) {
    // Create a temporary link
    let link = document.createElement('a');
    // Convert the canvas to data URL
    let dataURL = img.canvas.toDataURL();
    // Set the href attribute of the link to the data URL
    link.href = dataURL;
    // Set the download attribute with the desired filename
    link.download = filename;
    // Append the link to the document
    document.body.appendChild(link);
    // Programmatically trigger a click on the link
    link.click();
    // Remove the link from the document
    document.body.removeChild(link);
}


// Function to decode the hidden message

// Function to decode the message by comparing color channels
function decodeMessage(originalImage, encodedImage) {
    let decodedMessage = "";
    originalImage.loadPixels();
    encodedImage.loadPixels();

    for (let i = 0; i < originalImage.pixels.length; i += 4) {
        for (let j = 0; j < 3; j++) {
            // Compare color channel values and append to the decoded message
            let originalValue = int(originalImage.pixels[i + j]);
            let encodedValue = int(encodedImage.pixels[i + j]);

            // If color channel values are different, append '1', otherwise, append '0'
            if (originalValue !== encodedValue) {
                decodedMessage += '1';
            } else {
                decodedMessage += '0';
            }
        }
    }

    // Convert the binary message to text
    let textMessage = binaryToText(decodedMessage);
    return textMessage;
}


// Function to convert binary to text
function binaryToText(binaryMessage) {
    let textMessage = "";
    for (let i = 0; i < binaryMessage.length; i += 8) {
        let byte = binaryMessage.substr(i, 8);
        textMessage += String.fromCharCode(parseInt(byte, 2));
    }
    return textMessage;
}

