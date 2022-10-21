<template>

    <BasePublicTemplate>
        <SignUpForm></SignUpForm>
        <TheLinks></TheLinks>
    </BasePublicTemplate>

</template>


<script>
import SignUpForm from "@/components/SignUpForm.vue";
import BasePublicTemplate from "@/components/BasePublicTemplate.vue";
import TheLinks from "@/components/TheLinks.vue";

export default {
    data() {
        return {};
    },
    components: { SignUpForm, BasePublicTemplate, TheLinks }
};
</script> 
