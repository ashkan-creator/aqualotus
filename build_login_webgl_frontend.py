#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_login_webgl_frontend.py
اجرا از داخل ~/aqualotus:
    cp ~/Downloads/build_login_webgl_frontend.py ~/aqualotus/
    cd ~/aqualotus
    python3 build_login_webgl_frontend.py

کارها:
  1. frontend/src/pages/LoginPage.jsx -> کامل بازنویسی می‌شه (بک‌آپ می‌گیره)
     - ایمیل/رمز و گوگل دقیقاً با همون منطق قبلی دست‌نخورده می‌مونن
     - تب جدید «ورود با شماره موبایل» با OTP اضافه می‌شه (دو مرحله: شماره -> کد)
     - پس‌زمینه‌ی نقطه‌ای WebGL (Three.js از CDN) با رنگ برند خودتون (نه سفید/سیاه)
     - رزولوشن canvas رو موبایل پایین‌تره تا لگ نده
     - ریسپانسیو کامل
  2. frontend/src/slices/usersApiSlice.js -> دو mutation جدید اضافه می‌شه:
     useRequestLoginOtpMutation, useVerifyLoginOtpMutation
  3. frontend/src/index.css -> استایل صفحه زیر مارکر جدید اضافه می‌شه (append، نه overwrite)

بعد از اجرا: سرور Vite رو کامل ری‌استارت کن (Ctrl+C و npm run dev) و تو Incognito تست کن.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "aqualotus"
FRONTEND = ROOT / "frontend" / "src"

results = []


def report(label, ok, note):
    results.append((label, ok, note))


# ---------------------------------------------------------------------------
# 1. LoginPage.jsx — full rewrite
# ---------------------------------------------------------------------------
login_page_path = FRONTEND / "pages" / "LoginPage.jsx"

NEW_LOGIN_PAGE = '''import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Form, Button, Row, Col, Container, Card } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import {
  useLoginMutation,
  useGoogleLoginMutation,
  useRequestLoginOtpMutation,
  useVerifyLoginOtpMutation,
} from '../slices/usersApiSlice'
import { setCredentials } from '../slices/authSlice'
import { toast } from 'react-toastify'
import Loader from '../components/ui/Loader'
import { FaLeaf } from 'react-icons/fa'
import { Helmet } from 'react-helmet-async'

const LoginPage = () => {
  const canvasRef = useRef(null)

  const [method, setMethod] = useState('password') // 'password' | 'otp'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [phone, setPhone] = useState('')
  const [otp, setOtp] = useState('')
  const [otpSent, setOtpSent] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)

  const dispatch = useDispatch()
  const navigate = useNavigate()

  const [login, { isLoading }] = useLoginMutation()
  const [googleLogin] = useGoogleLoginMutation()
  const [requestLoginOtp, { isLoading: isSendingOtp }] = useRequestLoginOtpMutation()
  const [verifyLoginOtp, { isLoading: isVerifyingOtp }] = useVerifyLoginOtpMutation()
  const { userInfo } = useSelector((state) => state.auth)

  const { search } = useLocation()
  const sp = new URLSearchParams(search)
  const redirect = sp.get('redirect') || '/'

  useEffect(() => {
    if (userInfo) navigate(redirect)
  }, [userInfo, redirect, navigate])

  // --- resend OTP cooldown timer ---
  useEffect(() => {
    if (resendCooldown <= 0) return
    const t = setInterval(() => setResendCooldown((c) => c - 1), 1000)
    return () => clearInterval(t)
  }, [resendCooldown])

  // --- WebGL animated dot background (Three.js loaded via CDN, no bundler dependency) ---
  useEffect(() => {
    let active = true
    let renderer, geometry, material, scene, camera, animationId

    const getBrandColorVec = () => {
      const raw = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim()
      const probe = document.createElement('div')
      probe.style.color = raw || '#2e7d32'
      document.body.appendChild(probe)
      const match = getComputedStyle(probe).color.match(/\\d+/g)
      document.body.removeChild(probe)
      if (!match) return [0.18, 0.49, 0.2]
      return [Number(match[0]) / 255, Number(match[1]) / 255, Number(match[2]) / 255]
    }

    const initThree = (THREE) => {
      if (!canvasRef.current || !active) return
      const canvas = canvasRef.current
      const isMobile = window.innerWidth < 768

      renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false })
      renderer.setPixelRatio(isMobile ? 1 : Math.min(window.devicePixelRatio, 2))
      renderer.setSize(window.innerWidth, window.innerHeight)

      scene = new THREE.Scene()
      camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1)

      const [r, g, b] = getBrandColorVec()

      const uniforms = {
        u_time: { value: 0 },
        u_resolution: { value: new THREE.Vector2(window.innerWidth * 2, window.innerHeight * 2) },
        u_opacities: { value: [0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 1.0] },
        u_colors: {
          value: [
            new THREE.Vector3(r, g, b),
            new THREE.Vector3(r, g, b),
            new THREE.Vector3(r, g, b),
            new THREE.Vector3(r, g, b),
            new THREE.Vector3(r, g, b),
            new THREE.Vector3(r, g, b),
          ],
        },
        u_total_size: { value: isMobile ? 26.0 : 20.0 },
        u_dot_size: { value: isMobile ? 5.0 : 6.0 },
      }

      material = new THREE.ShaderMaterial({
        vertexShader: `
          precision mediump float;
          uniform vec2 u_resolution;
          out vec2 fragCoord;
          void main() {
            gl_Position = vec4(position, 1.0);
            fragCoord = (position.xy + 1.0) * 0.5 * u_resolution;
            fragCoord.y = u_resolution.y - fragCoord.y;
          }
        `,
        fragmentShader: `
          precision mediump float;
          in vec2 fragCoord;
          uniform float u_time;
          uniform float u_opacities[10];
          uniform vec3 u_colors[6];
          uniform float u_total_size;
          uniform float u_dot_size;
          uniform vec2 u_resolution;
          out vec4 fragColor;

          float PHI = 1.61803398874989484820459;
          float random(vec2 xy) {
              return fract(tan(distance(xy * PHI, xy) * 0.5) * xy.x);
          }

          void main() {
              vec2 st = fragCoord.xy;
              st.x -= abs(floor((mod(u_resolution.x, u_total_size) - u_dot_size) * 0.5));
              st.y -= abs(floor((mod(u_resolution.y, u_total_size) - u_dot_size) * 0.5));

              float opacity = step(0.0, st.x) * step(0.0, st.y);
              vec2 st2 = vec2(int(st.x / u_total_size), int(st.y / u_total_size));

              float frequency = 5.0;
              float show_offset = random(st2);
              float rand = random(st2 * floor((u_time / frequency) + show_offset + frequency));
              opacity *= u_opacities[int(rand * 10.0)];
              opacity *= 1.0 - step(u_dot_size / u_total_size, fract(st.x / u_total_size));
              opacity *= 1.0 - step(u_dot_size / u_total_size, fract(st.y / u_total_size));

              vec3 color = u_colors[int(show_offset * 6.0)];

              float animation_speed_factor = 3.0;
              vec2 center_grid = u_resolution / 2.0 / u_total_size;
              float dist_from_center = distance(center_grid, st2);
              float timing_offset_intro = dist_from_center * 0.01 + (random(st2) * 0.15);

              opacity *= step(timing_offset_intro, u_time * animation_speed_factor);
              opacity *= clamp((1.0 - step(timing_offset_intro + 0.1, u_time * animation_speed_factor)) * 1.25, 1.0, 1.25);

              fragColor = vec4(color, opacity);
              fragColor.rgb *= fragColor.a;
          }
        `,
        uniforms,
        glslVersion: THREE.GLSL3,
        blending: THREE.CustomBlending,
        blendSrc: THREE.SrcAlphaFactor,
        blendDst: THREE.OneFactor,
        transparent: true,
      })

      geometry = new THREE.PlaneGeometry(2, 2)
      const mesh = new THREE.Mesh(geometry, material)
      scene.add(mesh)

      const startTime = performance.now()
      const animate = () => {
        if (!active) return
        animationId = requestAnimationFrame(animate)
        uniforms.u_time.value = (performance.now() - startTime) / 1000
        renderer.render(scene, camera)
      }
      animate()

      const handleResize = () => {
        renderer.setSize(window.innerWidth, window.innerHeight)
        uniforms.u_resolution.value.set(window.innerWidth * 2, window.innerHeight * 2)
      }
      window.addEventListener('resize', handleResize)
      return () => window.removeEventListener('resize', handleResize)
    }

    let cleanupResize
    if (window.THREE) {
      cleanupResize = initThree(window.THREE)
    } else {
      const script = document.createElement('script')
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'
      script.async = true
      script.onload = () => {
        if (window.THREE) cleanupResize = initThree(window.THREE)
      }
      document.head.appendChild(script)
    }

    return () => {
      active = false
      if (cleanupResize) cleanupResize()
      if (animationId) cancelAnimationFrame(animationId)
      if (renderer) renderer.dispose()
      if (geometry) geometry.dispose()
      if (material) material.dispose()
    }
  }, [])

  const submitHandler = async (e) => {
    e.preventDefault()
    try {
      const res = await login({ email, password }).unwrap()
      dispatch(setCredentials({ ...res }))
      navigate(redirect)
    } catch (err) {
      toast.error(err?.data?.message || 'خطا در ورود')
    }
  }

  const requestOtpHandler = async (e) => {
    if (e) e.preventDefault()
    if (!phone) return
    try {
      await requestLoginOtp({ phone }).unwrap()
      toast.success('کد تایید برای شما پیامک شد')
      setOtpSent(true)
      setResendCooldown(60)
    } catch (err) {
      toast.error(err?.data?.message || 'ارسال کد با خطا مواجه شد')
    }
  }

  const verifyOtpHandler = async (e) => {
    e.preventDefault()
    try {
      const res = await verifyLoginOtp({ phone, otp }).unwrap()
      dispatch(setCredentials({ ...res }))
      navigate(redirect)
    } catch (err) {
      toast.error(err?.data?.message || 'کد تایید نادرست است')
    }
  }

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
    if (!clientId) return

    const handleGoogleResponse = async (response) => {
      try {
        const res = await googleLogin({ credential: response.credential }).unwrap()
        dispatch(setCredentials({ ...res }))
        navigate(redirect)
      } catch (err) {
        toast.error(err?.data?.message || 'خطا در ورود با گوگل')
      }
    }

    let cancelled = false
    const initGoogle = () => {
      if (cancelled) return
      if (window.google?.accounts?.id) {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleGoogleResponse,
        })
        const el = document.getElementById('google-signin-button')
        if (el) {
          window.google.accounts.id.renderButton(el, {
            theme: 'outline',
            size: 'large',
            width: 320,
            locale: 'fa',
          })
        }
      } else {
        setTimeout(initGoogle, 200)
      }
    }
    initGoogle()

    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <>
      <Helmet><title>ورود | AquaLotus</title></Helmet>
      <div className='aq-auth-webgl-wrapper'>
        <canvas ref={canvasRef} className='aq-auth-webgl-canvas' />
        <div className='aq-auth-vignette' />
        <Container className='aq-auth-container py-5'>
          <Row className='justify-content-center'>
            <Col xs={12} sm={10} md={7} lg={5} xl={4}>
              <Card className='auth-card aq-auth-card'>
                <Card.Body className='p-4'>
                  <div className='text-center mb-4'>
                    <FaLeaf className='auth-icon' />
                    <h2 className='auth-title'>ورود به حساب</h2>
                  </div>

                  <div className='aq-auth-method-switch mb-4'>
                    <button
                      type='button'
                      className={`aq-auth-method-btn ${method === 'password' ? 'active' : ''}`}
                      onClick={() => setMethod('password')}
                    >
                      ایمیل و رمز عبور
                    </button>
                    <button
                      type='button'
                      className={`aq-auth-method-btn ${method === 'otp' ? 'active' : ''}`}
                      onClick={() => setMethod('otp')}
                    >
                      ورود با شماره موبایل
                    </button>
                  </div>

                  {method === 'password' && (
                    <Form onSubmit={submitHandler}>
                      <Form.Group className='mb-3'>
                        <Form.Label>ایمیل</Form.Label>
                        <Form.Control
                          type='email'
                          placeholder='ایمیل خود را وارد کنید'
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                        />
                      </Form.Group>

                      <Form.Group className='mb-4'>
                        <Form.Label>رمز عبور</Form.Label>
                        <Form.Control
                          type='password'
                          placeholder='رمز عبور خود را وارد کنید'
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                        />
                      </Form.Group>

                      <div className='text-center mb-3'>
                        <Link to='/forgot-password' className='auth-link' style={{ fontSize: '0.9rem' }}>
                          رمز عبور را فراموش کرده‌اید؟
                        </Link>
                      </div>

                      <Button type='submit' className='w-100 btn-aqualotus' disabled={isLoading}>
                        {isLoading ? 'در حال ورود...' : 'ورود'}
                      </Button>
                      {isLoading && <Loader />}
                    </Form>
                  )}

                  {method === 'otp' && !otpSent && (
                    <Form onSubmit={requestOtpHandler}>
                      <Form.Group className='mb-4'>
                        <Form.Label>شماره موبایل</Form.Label>
                        <Form.Control
                          type='tel'
                          inputMode='numeric'
                          placeholder='مثال: 09123456789'
                          value={phone}
                          onChange={(e) => setPhone(e.target.value)}
                          required
                        />
                      </Form.Group>
                      <Button type='submit' className='w-100 btn-aqualotus' disabled={isSendingOtp}>
                        {isSendingOtp ? 'در حال ارسال...' : 'ارسال کد تایید'}
                      </Button>
                      {isSendingOtp && <Loader />}
                    </Form>
                  )}

                  {method === 'otp' && otpSent && (
                    <Form onSubmit={verifyOtpHandler}>
                      <div className='text-center mb-3 text-muted' style={{ fontSize: '0.9rem' }}>
                        کد ارسال شده به {phone} را وارد کنید
                      </div>
                      <Form.Group className='mb-4'>
                        <Form.Label>کد تایید</Form.Label>
                        <Form.Control
                          type='text'
                          inputMode='numeric'
                          maxLength={6}
                          className='otp-input'
                          value={otp}
                          onChange={(e) => setOtp(e.target.value)}
                          required
                        />
                      </Form.Group>
                      <Button type='submit' className='w-100 btn-aqualotus' disabled={isVerifyingOtp}>
                        {isVerifyingOtp ? 'در حال بررسی...' : 'تایید و ورود'}
                      </Button>
                      {isVerifyingOtp && <Loader />}

                      <div className='text-center mt-3'>
                        {resendCooldown > 0 ? (
                          <span className='text-muted' style={{ fontSize: '0.85rem' }}>
                            ارسال مجدد کد تا {resendCooldown} ثانیه دیگر
                          </span>
                        ) : (
                          <button type='button' className='aq-auth-link-btn' onClick={requestOtpHandler}>
                            ارسال مجدد کد
                          </button>
                        )}
                      </div>
                    </Form>
                  )}

                  <div className='d-flex align-items-center my-3'>
                    <hr className='flex-grow-1' />
                    <span className='mx-2 text-muted' style={{ fontSize: '0.85rem' }}>یا</span>
                    <hr className='flex-grow-1' />
                  </div>

                  <div className='d-flex justify-content-center'>
                    <div id='google-signin-button' />
                  </div>

                  <Row className='mt-3'>
                    <Col className='text-center'>
                      <span>حساب ندارید؟ </span>
                      <Link to={redirect ? `/register?redirect=${redirect}` : '/register'}>
                        ثبت‌نام کنید
                      </Link>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  )
}

export default LoginPage
'''

if login_page_path.exists():
    backup = login_page_path.with_suffix(login_page_path.suffix + ".pre-otplogin-redesign-backup")
    shutil.copy2(login_page_path, backup)
    login_page_path.write_text(NEW_LOGIN_PAGE, encoding="utf-8")
    report("LoginPage.jsx", True, f"بازنویسی کامل شد — بک‌آپ: {backup.name}")
else:
    report("LoginPage.jsx", False, f"فایل پیدا نشد: {login_page_path}")

# ---------------------------------------------------------------------------
# 2. usersApiSlice.js — add two mutations
# ---------------------------------------------------------------------------
api_slice_path = FRONTEND / "slices" / "usersApiSlice.js"

if api_slice_path.exists():
    content = api_slice_path.read_text(encoding="utf-8")
    backup = api_slice_path.with_suffix(api_slice_path.suffix + ".pre-otplogin-backup")

    old_endpoint_anchor = "    profile: builder.mutation({"
    new_endpoints = (
        "    requestLoginOtp: builder.mutation({\n"
        "      query: (data) => ({\n"
        "        url: `${USERS_URL}/login-otp/request`,\n"
        "        method: 'POST',\n"
        "        body: data,\n"
        "      }),\n"
        "    }),\n"
        "    verifyLoginOtp: builder.mutation({\n"
        "      query: (data) => ({\n"
        "        url: `${USERS_URL}/login-otp/verify`,\n"
        "        method: 'POST',\n"
        "        body: data,\n"
        "      }),\n"
        "    }),\n"
        "    profile: builder.mutation({"
    )

    old_export_anchor = "  useVerifyOtpAndResetMutation,\n  useProfileMutation,"
    new_export = (
        "  useVerifyOtpAndResetMutation,\n"
        "  useRequestLoginOtpMutation,\n"
        "  useVerifyLoginOtpMutation,\n"
        "  useProfileMutation,"
    )

    if content.count(old_endpoint_anchor) == 1 and content.count(old_export_anchor) == 1:
        shutil.copy2(api_slice_path, backup)
        content = content.replace(old_endpoint_anchor, new_endpoints)
        content = content.replace(old_export_anchor, new_export)
        api_slice_path.write_text(content, encoding="utf-8")
        report("usersApiSlice.js", True, f"دو mutation جدید اضافه شد — بک‌آپ: {backup.name}")
    else:
        report("usersApiSlice.js", False, "لنگر پیدا نشد یا تکراریه — هیچ تغییری اعمال نشد")
else:
    report("usersApiSlice.js", False, f"فایل پیدا نشد: {api_slice_path}")

# ---------------------------------------------------------------------------
# 3. index.css — append new styles under a version marker
# ---------------------------------------------------------------------------
index_css_path = FRONTEND / "index.css"

NEW_CSS = '''

/* --- login page webgl redesign v1 --- */
.aq-auth-webgl-wrapper {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  background: #050505;
}

.aq-auth-webgl-canvas {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.aq-auth-vignette {
  position: absolute;
  inset: 0;
  z-index: 1;
  background: radial-gradient(circle at center, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.15) 100%);
  pointer-events: none;
}

.aq-auth-container {
  position: relative;
  z-index: 2;
}

.aq-auth-card {
  backdrop-filter: blur(6px);
  background: rgba(255, 255, 255, 0.97);
}

.aq-auth-method-switch {
  display: flex;
  gap: 6px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 999px;
  padding: 4px;
}

.aq-auth-method-btn {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0.5rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--primary-dark, #2e7d32);
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.aq-auth-method-btn.active {
  background: var(--primary, #2e7d32);
  color: #fff;
}

.aq-auth-link-btn {
  background: none;
  border: none;
  padding: 0;
  color: var(--primary, #2e7d32);
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: underline;
}

@media (max-width: 576px) {
  .aq-auth-card {
    background: rgba(255, 255, 255, 0.99);
  }
  .aq-auth-method-btn {
    font-size: 0.78rem;
    padding: 0.45rem 0.5rem;
  }
}
'''

if index_css_path.exists():
    content = index_css_path.read_text(encoding="utf-8")
    if "/* --- login page webgl redesign v1 --- */" in content:
        report("index.css", False, "این مارکر قبلاً وجود داره — برای جلوگیری از تکرار چیزی اضافه نشد")
    else:
        backup = index_css_path.with_suffix(index_css_path.suffix + ".pre-otplogin-css-backup")
        shutil.copy2(index_css_path, backup)
        with open(index_css_path, "a", encoding="utf-8") as f:
            f.write(NEW_CSS)
        report("index.css", True, f"استایل جدید append شد — بک‌آپ: {backup.name}")
else:
    report("index.css", False, f"فایل پیدا نشد: {index_css_path}")

# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("گزارش نهایی:")
print("=" * 60)
ok_count = 0
for label, ok, note in results:
    mark = "✓" if ok else "✗"
    print(f"{mark} {label} — {note}")
    if ok:
        ok_count += 1
print("=" * 60)
if ok_count == len(results):
    print("همه‌چیز با موفقیت اعمال شد.")
    print("قدم بعدی: سرور Vite رو کامل ری‌استارت کن (Ctrl+C و npm run dev) و تو Incognito تست کن.")
else:
    print(f"⚠️  {len(results) - ok_count} مورد ناموفق بود.")
    sys.exit(1)
