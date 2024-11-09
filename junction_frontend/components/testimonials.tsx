"use client";

import { useState, useEffect } from 'react'
import useMasonry from "@/utils/useMasonry";
import Image, { StaticImageData } from "next/image";
import TestimonialImg01 from "@/public/images/testimonial-01.jpg";
import ClientImg01 from "@/public/images/client-logo-01.svg";

interface Testimonials {
  data: any;
}

interface Report {
  testimonialsData: any[];
}

const testimonialsDefault = [
  {
    testimonialsData: []
  }]


export default function Testimonials({ testimonialsData }: Report) {
  const masonryContainer = useMasonry();
  const [category, setCategory] = useState<number>(1);
  const [testimonials, setTestimonials] = useState<Report[]>([
    {
      testimonialsData: []
    },
  ]);

  useEffect(() => {
    setTestimonials(testimonialsData);
  }, [testimonialsData]);
  console.log(testimonials);
  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6">
      <div className="border-t py-12 [border-image:linear-gradient(to_right,transparent,theme(colors.slate.400/.25),transparent)1] md:py-20">
        {/* Section header */}
        <div className="mx-auto max-w-3xl pb-12 text-center">
          <h2 className="animate-[gradient_6s_linear_infinite] bg-[linear-gradient(to_right,theme(colors.gray.200),theme(colors.indigo.200),theme(colors.gray.50),theme(colors.indigo.300),theme(colors.gray.200))] bg-[length:200%_auto] bg-clip-text pb-4 font-nacelle text-3xl font-semibold text-transparent md:text-4xl">
            Don't take our word for it
          </h2>
          <p className="text-lg text-indigo-200/65">
            We provide tech-first solutions that empower decision-makers to
            build healthier and happier workspaces from anywhere in the world.
          </p>
        </div>

        {/* <div> */}
          {/* Buttons */}
         

          {/* Cards */}
          <div
            className="mx-auto max-w-sm items-start gap-6 sm:max-w-none sm:grid-cols-2 lg:grid-cols-3"
            ref={masonryContainer}
          >
          {testimonials && testimonials.length > 0 ? 
            testimonials.map((testimonial, index) => (
              <div key={index} className="group">
                <Testimonial report = {testimonial} category={category}>
                  {testimonial.testimonialsData}
                </Testimonial>
              </div>
            ))
            : 
            <div>No testimonials available</div>
          }
          </div>
        {/* </div> */}
      </div>
    </div>
  );
}

export function Testimonial({
  report,
  category,
  children,
}: {
  report: {
    testimonialsData: any[];
  };
  category: number;
  children: React.ReactNode;
}) {
  return (
    <article
      className={`relative rounded-2xl bg-gradient-to-br from-gray-900/50 via-gray-800/25 to-gray-900/50 p-5 backdrop-blur-sm transition-opacity before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,theme(colors.gray.800),theme(colors.gray.700),theme(colors.gray.800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)]`}
    >
      <div className="flex flex-col gap-4">
        <div>
          {/* <Image src={report.testimonialsData[0]} height={36} alt="Client logo" /> */}
        </div>
        <p className="text-indigo-200/65 before:content-['“'] after:content-['”']">
          {children}
        </p>
        <div className="flex items-center gap-3">
          {/* <Image
            className="inline-flex shrink-0 rounded-full"
            src={report.testimonialsData[0]}
            width={36}
            height={36}
            alt={report.testimonialsData[0]}
          /> */}
          <div className="text-sm font-medium text-gray-200">
            <span>{report.testimonialsData}</span>
            <span className="text-gray-700"> - </span>
            <a
              className="text-indigo-200/65 transition-colors hover:text-indigo-500"
              href="#0"
            >
              {report.testimonialsData[0]}
            </a>
          </div>
        </div>
      </div>
    </article>
  );
}

