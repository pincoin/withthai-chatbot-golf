Date.prototype.formatDate = function () {
    return this.getFullYear()
        + '-' + ('0' + (this.getMonth() + 1)).slice(-2)
        + '-' + ('0' + this.getDate()).slice(-2);
}

HTMLElement.prototype.show = function () {
    if (this.classList.contains('is-hidden')) {
        this.classList.remove('is-hidden');
    }
}

HTMLElement.prototype.hide = function () {
    if (!this.classList.contains('is-hidden')) {
        this.textContent = '';
        this.classList.add('is-hidden');
    }
}

HTMLElement.prototype.toggle = function () {
    if (this.classList.contains('is-hidden')) {
        this.classList.remove('is-hidden');
    } else {
        this.textContent = '';
        this.classList.add('is-hidden');
    }
}

HTMLElement.prototype.error_field = function () {
    if (!this.classList.contains('is-danger')) {
        this.classList.add('is-danger');
    }
}

HTMLElement.prototype.clear_error_field = function () {
    if (this.classList.contains('is-danger')) {
        this.classList.remove('is-danger');
    }
}