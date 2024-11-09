export const metadata = {
  title: "Home - Open PRO",
  description: "Page description",
};

import PageIllustration from "@/components/page-illustration";
import GoogleMapView from "@/components/google-map";
// import Workflows from "@/components/workflows";
// import Features from "@/components/features";
import Testimonials from "@/components/testimonials";
// import Cta from "@/components/cta";

export default function Home() {
  return (
    <>
      <PageIllustration />
      <div className="mt-20 h-[500px] w-full flex items-center justify-center bg-gray-900/90 rounded-lg">    
        <GoogleMapView />
      </div>
      <Testimonials />
      {/* <Hero />
      <Workflows />
      <Features />
      <Cta /> */}
    </>
  );
}
