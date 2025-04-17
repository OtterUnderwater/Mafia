<template>
    <button :class="['button-role', roleColorClass]" @click="handleClick">
        {{ buttonLabel }} 
    </button>
</template>

<script>
import { RoleEnum, StatusEnum } from '@/constants/enums.js';

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
        idStage: {
            type: Number,
            required: true,
        },
    },
    computed: {
        buttonLabel() {
            let label = '';
            if (this.item.showNickname)
                if (!this.$store.state.anonymousGame)
                    label = `${this.item.nickname}\n${this.item.role}`;   
                else
                    label = `${this.item.id}\n${this.item.role}`;    
            else
                label = `${this.index + 1}`;
            if (this.item.status === StatusEnum.DEAD)
                label += `\n${this.item.elimination_reason}`;
            else if (this.item.fouls > 0)
                label += `\nfoul: ${this.item.fouls}`;    
            return label;
        },

        roleColorClass() {
            if (this.item.status == StatusEnum.DEAD)
                return 'color-dead';
            if (this.idStage === 0 && (this.item.role === RoleEnum.MAFIA || this.item.role === RoleEnum.DON))
                return 'color-mafia-don';
            if (this.idStage === 1 && this.item.role === RoleEnum.SHERIFF)
                return 'color-sheriff';
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

<style scoped lang="scss">
@use "@/assets/styles/colors" as *;

.button-role {
    border-radius: 4px;
    background-color: #ffffff;
    color: black;
    border: 1px solid black;
    padding: 10px;
    cursor: pointer;
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    white-space: pre-line;
    word-break: break-word;
}

.color-mafia-don {
    background-color: $black;
    color: $red;
    border: 1px solid $red;
}

.color-sheriff {
    background-color: $red;
    color: $black;
    border: 1px solid $black;
}

.color-dead {
    background-color: $dead-player;
    color: $black;
    border: 1px solid $black;
}
</style>