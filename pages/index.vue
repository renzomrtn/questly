<template>
    <section>
        <div class="words">
            <p>Finish quest, earn EXP!</p><br/>
            <h1>Welcome to Questly</h1>
            <p>Where your quests awaits!</p>
        </div>
        <div class="buttons">
            <v-button class="login">
                Sign In
            </v-button>
            <v-button class="signup">
                Sign Up
            </v-button>
        </div>
    </section>
    <section>
        <p>Questly is a productivity tool that encourages people to create and work on their day-to-day tasks to gain EXP.</p>
    </section>
</template>
<style scoped>
section {
    align-items: center;
    text-align: center;
    justify-content: center;
}
.buttons {
    width: fit-content;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    border: 1px solid lightgray;
    border-radius: 12px;
    padding: 16px;
    align-items: center;
}
v-button {
    padding: 18px 28px;
    text-align: center;
    justify-content: center;
    border-radius: 12px;
    width: 8rem;
    height: fit-content;
}
.login {
    background-color: blue;
    border: 1px solid grey;
    color: white;
}
.signup {
    border: 1px solid blue;
    color: blue;
}
</style>