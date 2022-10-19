<template>

    <BasePublicTemplate>
        <ForgotPasswordForm></ForgotPasswordForm>
        <TheLinks></TheLinks>
    </BasePublicTemplate>

</template>


<script>
import BasePublicTemplate from "@/components/BasePublicTemplate.vue";
import ForgotPasswordForm from "@/components/ForgotPasswordForm.vue";
import TheLinks from "@/components/TheLinks.vue";

export default {
    data() {
        return {};
    },
    components: { BasePublicTemplate, ForgotPasswordForm, TheLinks }
};
</script> 
