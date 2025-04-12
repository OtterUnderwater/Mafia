<template>
    <button :class="['button-role', roleColorClass]" @click="handleClick">
        {{ item.showNickname ? item.nickname + '\n' + item.role : index + 1 }}
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
        currentRole: {
            type: String,
            default: null,
        },
    },

    computed: {
        roleColorClass() {
            if (this.currentRole != null) {
                if (this.currentRole == this.item.role) {
                    if (this.currentRole === 'Mafia' || this.currentRole === 'Don')
                        return 'color-mafia-don';
                    if (this.currentRole === 'Sheriff')
                        return 'color-sheriff';
                }
            }
            return '';
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

.color-mafia-don {
    background-color: #1e1e1e;
    color: #dc2a0b;
    border: 1px solid #dc2a0b;
}

.color-sheriff {
    background-color: #dc2a0b;
    color: #1e1e1e;
    border: 1px solid #1e1e1e;
}
</style>