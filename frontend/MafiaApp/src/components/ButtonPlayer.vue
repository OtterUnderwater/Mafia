<template>
    <button class="button-role" @click="handleClick">
        {{ showNickname ? item.nickname : index + 1 }}
    </button>
</template>

<script>
export default {
    props: {
        item: {
            type: Object,
            required: true,
        },
        index: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            showNickname: false
        }
    },
    methods: {
        handleClick() {
            this.$emit('show-player', this.index);
        },
    },
};
</script>

<style scoped>
.button-role {
    background-color: white;
    color: black;
    border: 1px solid black;
    padding: 10px;
    cursor: pointer;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
</style>