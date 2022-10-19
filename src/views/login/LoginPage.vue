<template>

    <BasePublicTemplate>
        <LoginForm></LoginForm>
        <TheLinks></TheLinks>
    </BasePublicTemplate>

</template>


<script>
import LoginForm from "@/components/LoginForm.vue";
import BasePublicTemplate from "@/components/BasePublicTemplate.vue";
import TheLinks from "@/components/TheLinks.vue";

export default {
    data() {
        return {};
    },
    components: { LoginForm, BasePublicTemplate, TheLinks }
};
</script> 
