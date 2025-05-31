const MONTH_NAMES_FULL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const MONTH_NAMES_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const DAY_NAMES_FULL = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const DAY_NAMES_ABBR = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

/**
 * Parsea una cadena de fecha y hora en formato "YYYY-MM-DD HH:mm".
 * @param {string} dateTimeStr - La cadena de fecha y hora.
 * @returns {Date|null} Un objeto Date si el parseo es exitoso, de lo contrario null.
 */
function parseDateTimeString(dateTimeStr) {
    const dateTimeRegex = /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$/;
    const match = dateTimeStr.match(dateTimeRegex);

    if (!match) return null;

    const year = parseInt(match[1], 10);
    const month = parseInt(match[2], 10) - 1; // Mes es 0-indexado en JS Date
    const day = parseInt(match[3], 10);
    const hour = parseInt(match[4], 10);
    const minute = parseInt(match[5], 10);

    const date = new Date(year, month, day, hour, minute);

    // Validar si los componentes forman una fecha válida
    if (
        date.getFullYear() !== year ||
        date.getMonth() !== month ||
        date.getDate() !== day ||
        date.getHours() !== hour ||
        date.getMinutes() !== minute
    ) {
        return null; // Componentes de fecha inválidos (ej. 2023-02-30)
    }
    return date;
}

/**
 * Formatea un objeto Date o una cadena de fecha (YYYY-MM-DD HH:mm) usando especificadores tipo strftime.
 * @param {Date|string} dateInput - El objeto Date o la cadena de fecha a formatear.
 * @param {string} formatStr - La cadena de formato (ej. "%Y-%m-%d %H:%M").
 * @returns {string} La cadena de fecha formateada o un mensaje de error si la entrada es inválida.
 */
export const formatDate = (dateInput, formatStr) => {
    let date;

    if (typeof dateInput === 'string') {
        date = parseDateTimeString(dateInput);
        if (!date) {
            console.error("Invalid date string provided:", dateInput, "- Expected format YYYY-MM-DD HH:mm");
            return "Invalid Date String";
        }
    } else if (dateInput instanceof Date) {
        if (isNaN(dateInput.getTime())) {
            console.error("Invalid Date object provided.");
            return "Invalid Date Object";
        }
        date = dateInput;
    } else {
        console.error("Invalid date input type. Expected string or Date object.");
        return "Invalid Input Type";
    }

    // Helper para obtener el día del año (1-366)
    const getDayOfYear = (d) => {
        const start = new Date(d.getFullYear(), 0, 0);
        const diff = d - start;
        const oneDay = 1000 * 60 * 60 * 24;
        return Math.floor(diff / oneDay);
    };

    // Helper para el número de semana %U (Domingo como primer día, semana 00-53)
    // Semana 01 es la semana con el primer Domingo. Días anteriores son semana 00.
    const getWeekU = (d) => {
        const year = d.getFullYear();
        const dateInYear = new Date(d.valueOf());
        dateInYear.setHours(0, 0, 0, 0);

        const firstDayOfYear = new Date(year, 0, 1);
        const firstDayOfYearWeekday = firstDayOfYear.getDay(); // 0 para Domingo

        let firstSunday = new Date(firstDayOfYear.valueOf());
        if (firstDayOfYearWeekday !== 0) {
            firstSunday.setDate(firstDayOfYear.getDate() + (7 - firstDayOfYearWeekday));
        }
        firstSunday.setHours(0, 0, 0, 0);

        if (dateInYear < firstSunday) return 0;
        const diffTime = dateInYear.getTime() - firstSunday.getTime();
        return Math.floor(diffTime / (1000 * 60 * 60 * 24 * 7)) + 1;
    };

    // Helper para el número de semana %W (Lunes como primer día, semana 00-53)
    // Semana 01 es la semana con el primer Lunes. Días anteriores son semana 00.
    const getWeekW = (d) => {
        const year = d.getFullYear();
        const dateInYear = new Date(d.valueOf());
        dateInYear.setHours(0, 0, 0, 0);

        const firstDayOfYear = new Date(year, 0, 1);
        const firstDayOfYearWeekday = firstDayOfYear.getDay(); // 1 para Lunes

        let firstMonday = new Date(firstDayOfYear.valueOf());
        if (firstDayOfYearWeekday === 0) { // Domingo
            firstMonday.setDate(firstDayOfYear.getDate() + 1);
        } else if (firstDayOfYearWeekday !== 1) { // No es Lunes
            firstMonday.setDate(firstDayOfYear.getDate() + ((1 - firstDayOfYearWeekday + 7) % 7));
        }
        firstMonday.setHours(0, 0, 0, 0);

        if (dateInYear < firstMonday) return 0;
        const diffTime = dateInYear.getTime() - firstMonday.getTime();
        return Math.floor(diffTime / (1000 * 60 * 60 * 24 * 7)) + 1;
    };

    let formattedString = "";
    for (let i = 0; i < formatStr.length; i++) {
        if (formatStr[i] === '%') {
            if (i + 1 < formatStr.length) {
                const specifier = formatStr[i + 1];
                let replacementFound = true;
                switch (specifier) {
                    case 'Y': formattedString += date.getFullYear(); break;
                    case 'y': formattedString += String(date.getFullYear() % 100).padStart(2, '0'); break;
                    case 'm': formattedString += String(date.getMonth() + 1).padStart(2, '0'); break;
                    case 'B': formattedString += MONTH_NAMES_FULL[date.getMonth()]; break;
                    case 'b': case 'h': formattedString += MONTH_NAMES_ABBR[date.getMonth()]; break;
                    case 'd': formattedString += String(date.getDate()).padStart(2, '0'); break;
                    case 'H': formattedString += String(date.getHours()).padStart(2, '0'); break;
                    case 'I': formattedString += String(((date.getHours() + 11) % 12) + 1).padStart(2, '0'); break;
                    case 'M': formattedString += String(date.getMinutes()).padStart(2, '0'); break;
                    case 'S': formattedString += String(date.getSeconds()).padStart(2, '0'); break;
                    case 'A': formattedString += DAY_NAMES_FULL[date.getDay()]; break;
                    case 'a': formattedString += DAY_NAMES_ABBR[date.getDay()]; break;
                    case 'p': formattedString += date.getHours() < 12 ? 'AM' : 'PM'; break;
                    case 'w': formattedString += date.getDay(); break; // Domingo=0, Sábado=6
                    case 'j': formattedString += String(getDayOfYear(date)).padStart(3, '0'); break;
                    case 'U': formattedString += String(getWeekU(date)).padStart(2, '0'); break;
                    case 'W': formattedString += String(getWeekW(date)).padStart(2, '0'); break;
                    case 'c': formattedString += date.toLocaleString(); break;
                    case 'x': formattedString += date.toLocaleDateString(); break;
                    case 'X': formattedString += date.toLocaleTimeString(); break;
                    case '%': formattedString += '%'; break;
                    default:
                        replacementFound = false; // No es un especificador conocido
                        formattedString += formatStr[i]; // Añade el '%' literal
                        break;
                }
                if (replacementFound) {
                    i++; // Avanza el índice para saltar el especificador
                }
            } else {
                // '%' es el último caracter en formatStr
                formattedString += formatStr[i];
            }
        } else {
            formattedString += formatStr[i];
        }
    }
    return formattedString;
};