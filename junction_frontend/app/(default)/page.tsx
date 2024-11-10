'use client'

// export const metadata = {
//   title: "Home - Open PRO",
//   description: "Page description",
// };

import { useEffect, useState } from "react";
import PageIllustration from "@/components/page-illustration";
import GoogleMapView from "@/components/google-map";
// import Workflows from "@/components/workflows";
// import Features from "@/components/features";
import Testimonials from "@/components/testimonials";
// import Cta from "@/components/cta";



export default function Home() {
  const [reportData, setReportData] = useState<String>('');
  const handlerCLick = (data: String) => {
    setReportData(data);
  }
  // use effect to refresh
  useEffect(() => {
    if(reportData != ""){
  
    }
  }, [reportData]);

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
