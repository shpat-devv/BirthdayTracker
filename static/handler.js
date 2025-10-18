let user_key = localStorage.getItem("user_key");

document.addEventListener("DOMContentLoaded", function() {
    if (!verifyUser()) {
        window.location.href = "/login";
    }
});

function verifyUser() {
    return user_key === "valid_user_key";
}

function logout() {
    localStorage.removeItem("user_key");
    window.location.href = "/login";
}