js = """function createGradioAnimation() {
    // Hauptcontainer für den Text
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2.5em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '5px';

    // Container für den Untertitel
    var subtitleContainer = document.createElement('div');
    subtitleContainer.id = 'gradio-subtitle';
    subtitleContainer.style.fontSize = '1.2em'; // Kleinere Schriftgröße für den Untertitel
    subtitleContainer.style.fontWeight = 'normal';
    subtitleContainer.style.marginTop = '2px'; // Geringerer Abstand zum oberen Text
    subtitleContainer.style.textAlign = 'center';
    subtitleContainer.style.marginBottom = '15px';

    // Haupttext und Untertitel
    var text = 'Welcome to KaraokeNet!';
    var text2 = 'Take your karaoke skills to the next level.';
    var delay = 150; // Verzögerung zwischen den Buchstaben
    var totalTime = 0; // Gesamtzeit für die erste Animation

    // Erste Schleife für den Haupttext
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * delay);
        })(i);
    }

    // Berechnung der Gesamtzeit für die erste Animation
    totalTime = text.length * delay;

    delay = 50; // Verzögerung für den Untertitel

    // Zweite Schleife für den Untertitel
    for (var j = 0; j < text2.length; j++) {
        (function(j){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text2[j];

                subtitleContainer.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, totalTime + (j * delay));
        })(j);
    }

    // Einfügen der Container in die Gradio-Oberfläche
    var gradioContainer = document.querySelector('.gradio-container');
    if (gradioContainer) {
        gradioContainer.insertBefore(container, gradioContainer.firstChild);
        gradioContainer.insertBefore(subtitleContainer, container.nextSibling);
    } else {
        console.error("gradio-container not found");
    }

    return 'Animation created';
}
"""

css = """.gr-dropdown {
    width: 300px;
    padding: 5px;
    font-size: 1em;
    border-radius: 5px;
    border: 1px solid #ccc;
}

.gr-button {
    background-color: #007BFF;
    color: #FFFFFF;
    border: none;
    padding: 15px 20px;
    border-radius: 15px;
    cursor: pointer;
    transition: background-color 0.3s;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
}

.gr-button img {
    width: 32px; /* Breite des Icons */
    height: 32px; /* Höhe des Icons */
    margin-right: 10px; /* Abstand zwischen Icon und Text */
}

.gr-button:hover {
    background-color: #0056b3;
}

/* Lässt Erklärung anzeigen, wenn die Maus des Benutzers auf den Buttons ist */
.gr-button-tooltip {
    visibility: hidden;
    white-space: nowrap; /* Keine Zeilenumbrüche */
    background-color: transparent;
    text-align: left;
    position: absolute;
    z-index: 1;
    top: 50%; /* Vertikal mittig */
    left: 7%; 
    transform: translateY(-50%);
    opacity: 0;
    transition: opacity 0.3s;
    font-style: italic; /* Text kursiv machen */
}

.gr-button-tooltip-right {
    left: auto; /* Reset left position */
    right: 7%; /* Position tooltip on the right */
}


.gr-button-container:hover .gr-button-tooltip {
    visibility: visible;
    opacity: 1;
}

.gr-row {
    flex-direction: row;
    justify-content: center;
    margin-top: 20px;
    width: 100%;
}

.gr-column {
    flex-direction: column;
    align-items: center;
    justify-content: center; /* Vertikal zentriert */
    margin: 0 10px;
}

.gr-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

.gr-textbox {
    background-color: #0c0f18;
    color: #FFFFFF;
    padding: 10px;
    margin: 10px;
    border-radius: 5px;
    text-align: center;
    width: fit-content;
    max-width: 100%;
}

.gr-audio-container {
    width: 100%; /* Container-Breite auf 100% setzen */
    max-width: 100%; /* Maximale Breite des Containers anpassen */
    margin: 0 auto; /* Zentrieren des Containers */
    padding: 10px;
    display: flex;
    justify-content: center; /* Zentrieren des Inhalts horizontal */
}

.gr-audio {
    width: 100%; /* Audio-Komponente auf 100% der Container-Breite setzen */
    max-width: 100%; /* Optional: maximale Breite festlegen */
    box-sizing: border-box; /* Box-Sizing auf Border-Box setzen */
}

"""
