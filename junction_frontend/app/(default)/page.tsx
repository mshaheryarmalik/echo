'use client'

// export const metadata = {
//   title: "Home - Open PRO",
//   description: "Page description",
// };

import PageIllustration from "@/components/page-illustration";
import GoogleMapView from "@/components/google-map";
// import Workflows from "@/components/workflows";
// import Features from "@/components/features";
import Testimonials from "@/components/testimonials";
// import Cta from "@/components/cta";



export default function Home() {
  let reportData: any = {};
  const handlerCLick = (data: any) => {
    console.log("data received :");
    console.log(data);
    reportData = data;
  }
  return (
    <>
      <PageIllustration />
      <GoogleMapView onDataReceived={handlerCLick} />
      <Testimonials reportData={reportData} />
      {/* <Hero />
      <Workflows />
      <Features />
      <Cta /> */}
    </>
  );
}
