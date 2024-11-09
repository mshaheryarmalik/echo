export const metadata = {
  title: "Home - Open PRO",
  description: "Page description",
};

import PageIllustration from "@/components/page-illustration";
import GoogleMapView from "@/components/google-map";
// import Workflows from "@/components/workflows";
// import Features from "@/components/features";
import Testimonials from "@/components/testimonials";
import Button from "@/components/button_view";
// import Cta from "@/components/cta";

export default function Home() {
  return (
    <>
      <PageIllustration />
        <GoogleMapView />
      <Testimonials />
      {/* <Hero />
      <Workflows />
      <Features />
      <Cta /> */}
    </>
  );
}
