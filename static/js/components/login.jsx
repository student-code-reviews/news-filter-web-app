"use strict";

class Login extends React.Component {
  render() {
    return (
        <h2>Login here: </h2>

        <form action = '/logged-in' method='POST' >
        User ID:<br>
        <input type="email" name="email" required>
        <br>
        Password:<br>
        <input type="password" name="password" required>
        <br><br>
        <input type="submit">
        </form>
    );
  }
}
